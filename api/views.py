from django.http import JsonResponse


def csrf_failure(request, reason=""):
	return JsonResponse({
		"detail": "CSRF verification failed. Request aborted.",
		"reason": "Invalid or missing CSRF token."
	}, status=403)

