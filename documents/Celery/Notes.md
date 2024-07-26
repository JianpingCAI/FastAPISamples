
# Celery

## Introduction

Celery is a widely adopted, production-ready **job queue library**.

## Dash Application Usage

[reference](https://dash.plotly.com/background-callbacks)

A Celery backend that runs callback logic in a Celery worker and returns results to the Dash app through a **Celery broker** like **Redis**.

This is recommended for production as, unlike Disk Cache, it queues the background callbacks, running them one-by-one in the order that they were received by dedicated Celery worker(s).

Celery is a widely adopted, production-ready **job queue library**.
