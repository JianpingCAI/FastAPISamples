
# Celery

## Introduction

Celery is a widely adopted, production-ready **job queue library**.

## Dash Application Usage

[reference](https://dash.plotly.com/background-callbacks)

A Celery backend that runs callback logic in a Celery worker and returns results to the Dash app through a **Celery broker** like **Redis**.

This is recommended for production as, unlike Disk Cache, it queues the background callbacks, running them one-by-one in the order that they were received by dedicated Celery worker(s).

Celery is a widely adopted, production-ready **job queue library**.

## Celery Anatomy

Celery Clients: This triggers the execution of the celery worker over the message broker. A web-request or any other interface on the terminal can be seen as a celery client.

Celery Workers: This represents the background task and the logic part of the celery. Regarding the implemented logic required by the developers will b processed in the worker. The results can be visualized either on the terminal or return to the calling function as in many web application.

Message Broker: The role of the broker is to establish the communication between celery client and celery worker through message queues. RabbitMQ and Redis are commonly utilized message brokers.
