import logging
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

JOB_ID = "collect_all"


def _crash_resilient(job_func: Callable[[], None]) -> Callable[[], None]:
    """Wraps a job so an exception in one run cannot stop the scheduler (AC-4)."""

    def wrapper() -> None:
        try:
            job_func()
        except Exception:
            logger.exception("scheduled run failed; scheduler continues")

    return wrapper


def build_scheduler(
    job_func: Callable[[], None],
    interval_minutes: int,
    *,
    run_immediately: bool = False,
    scheduler: BackgroundScheduler | None = None,
) -> BackgroundScheduler:
    """Builds (but does not start) a scheduler that runs job_func every interval_minutes."""
    sched = scheduler or BackgroundScheduler()
    trigger = IntervalTrigger(minutes=interval_minutes)

    add_job_kwargs = {}
    if run_immediately:
        add_job_kwargs["next_run_time"] = datetime.now(trigger.timezone)

    sched.add_job(_crash_resilient(job_func), trigger, id=JOB_ID, **add_job_kwargs)
    return sched
