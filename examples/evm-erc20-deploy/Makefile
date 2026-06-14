.PHONY: smoke-test validate simulate

smoke-test:
	python scripts/validate-skills.py

validate:
	python scripts/check_readiness.py
	python scripts/validate_token.py

simulate:
	python scripts/simulate_deploy.py