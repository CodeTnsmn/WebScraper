from datetime import datetime, timedelta

from webscraper.schedule import JOB_ID, build_scheduler


def test_interval_trigger_matches_requested_minutes_ac1():
    sched = build_scheduler(lambda: None, interval_minutes=5)

    job = sched.get_job(JOB_ID)

    assert job.trigger.interval == timedelta(minutes=5)


def test_job_func_triggers_registered_callable_ac2():
    calls = []
    sched = build_scheduler(lambda: calls.append(1), interval_minutes=60)

    sched.get_job(JOB_ID).func()

    assert calls == [1]


def test_run_immediately_schedules_close_to_now_ac3():
    sched = build_scheduler(lambda: None, interval_minutes=30, run_immediately=True)

    job = sched.get_job(JOB_ID)

    assert abs((job.next_run_time.replace(tzinfo=None) - datetime.now()).total_seconds()) < 2


def test_without_run_immediately_first_run_is_about_one_interval_away_ac3():
    sched = build_scheduler(lambda: None, interval_minutes=30, run_immediately=False)
    # next_run_time is only computed once the scheduler starts (APScheduler pending-job
    # behavior) — start/shutdown immediately to read it without the job actually firing.
    sched.start()
    job = sched.get_job(JOB_ID)
    delta_seconds = (job.next_run_time.replace(tzinfo=None) - datetime.now()).total_seconds()
    sched.shutdown(wait=False)

    assert 29 * 60 < delta_seconds <= 30 * 60


def test_exception_in_job_is_swallowed_by_wrapper_ac4():
    def boom():
        raise RuntimeError("boom")

    sched = build_scheduler(boom, interval_minutes=60)

    sched.get_job(JOB_ID).func()  # must not raise


def test_shutdown_sets_running_false_ac5():
    sched = build_scheduler(lambda: None, interval_minutes=60)
    sched.start()
    assert sched.running is True

    sched.shutdown(wait=False)

    assert sched.running is False
