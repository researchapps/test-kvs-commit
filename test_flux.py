#!/usr/bin/env python3

import flux
import flux.job
import json


def test_kvs_commit():
    """
    This will retrieve the burstable job, update the
    spec to remove burstable via kvs.commit, and then check to see
    if it's there.
    """
    print("\n==== TESTING UPDATING A JOBSPEC")

    # Get all jobs (we should only have one)
    handle = flux.Flux()
    jobs = flux.job.job_list(handle).get()
    print("\nFound jobs:")
    print(json.dumps(jobs, indent=4))
    job = jobs["jobs"][0]

    # Get the current job spec
    print("\n🦊️ Initial jobspec")
    kvs = flux.job.job_kvs(handle, job["id"])
    spec = kvs.get("jobspec")
    print(json.dumps(spec, indent=4))

    print("\n🤪️ Removing burstable...")
    del spec["attributes"]["system"]["burstable"]
    kvs = flux.job.job_kvs(handle, job["id"])

    print("\n🧐️ Confirm it's not there!")
    print(json.dumps(spec, indent=4))
    assert "bustable" not in spec["attributes"]["system"]

    print("\n🧝‍♀️️ Updating the spec in kvs and committing!")
    kvs["jobspec"] = spec
    kvs.commit()

    print("🦾️ Re-retrieving the kvs and spec...")
    kvs = flux.job.job_kvs(handle, job["id"])
    spec = kvs.get("jobspec")

    print("🧐️ Is burstable there?")
    print(json.dumps(spec, indent=4))
    assert "burstable" not in spec["attributes"]["system"]


def test_adding_attribute():
    """
    This will test adding an attribute directly to the KVS.
    """
    print("\n==== TESTING ADDING AN ATTRIBUTE TO KVS")
    # Get all jobs (we should only have one)
    handle = flux.Flux()
    jobs = flux.job.job_list(handle).get()
    print("\nFound jobs:")
    print(json.dumps(jobs, indent=4))
    job = jobs["jobs"][0]
    kvs = flux.job.job_kvs(handle, job["id"])

    print("\n🧝‍♀️️ Adding a new variable to the kvs and committing!")
    # Weird that this doesn't even stick!
    # I tried an integer, a string, and a boolean
    kvs["burstable"] = 1
    value = kvs.get("burstable")
    print(f"Found value {value}")
    kvs.commit()

    print("🦾️ Re-retrieving the kvs...")
    kvs = flux.job.job_kvs(handle, job["id"])
    print("🧐️ Is burstable there?")
    value = kvs.get("burstable")
    print(f"Found value {value}")
    assert kvs.get("burstable")
