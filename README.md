# Udemy REST API Course Code

---

A step-by-step build of a REST API using python's Flask and SQLAlchemy, as taught by Jose Salvatierra on Udemy.
Some minor differences with main course code are present.

## Docker

You can launch the stack on Docker Swarm like so:

```
$ docker image build --rm -t stores .
$ docker stack deploy -c docker-compose.yml storeapi
```

To remove:

```
$ docker stack rm storeapi
```

NOTE: You will still have to manually remove volumes `pg_data` and `pg_backups` created by the stack.