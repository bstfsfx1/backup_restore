# education/views.py
from django.shortcuts import render
from .models import Course, Tutor, School #, Curriculum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess
import os
import sys

# List of allowed scripts
VALID_SCRIPTS = {
    "export": "export_all.py",
    "import": "import_all.py",
    "format": "format_data.py",
    "clear": "clear_data.py"
}

# Path to scripts folder
SCRIPTS_DIR = os.path.join(settings.BASE_DIR, 'templates/education/scripts')

@csrf_exempt
def run_script_view(request):
    """AJAX endpoint to run Python scripts"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST required"}, status=400)

    action = request.POST.get("action")
    if action not in VALID_SCRIPTS:
        return JsonResponse({"success": False, "error": "Invalid action"}, status=400)

    script_name = VALID_SCRIPTS[action]
    script_path = os.path.join(SCRIPTS_DIR, script_name)

    if not os.path.exists(script_path):
        return JsonResponse({"success": False, "error": f"Script not found: {script_name}"}, status=404)

    try:
        # Run script with DB_PASSWORD
        env = os.environ.copy()
        env["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "")

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=SCRIPTS_DIR,
            env=env
        )

        output = (result.stdout + result.stderr).strip()
        return JsonResponse({
            "success": result.returncode == 0,
            "output": output or "Completed.",
            "error": result.stderr.strip() if result.stderr else None
        })

    except subprocess.TimeoutExpired:
        return JsonResponse({"success": False, "error": "Script timed out"}, status=500)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def data_man(request):
    # """Main data manager page with 4 buttons"""
    return render(request, 'education/data_man.html')