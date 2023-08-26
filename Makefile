.PHONY: test

test:
	docker compose -f test.yml up -d && pytest && docker compose down