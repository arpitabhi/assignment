docker rm -f devPostgres ; docker run -d --name devPostgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
