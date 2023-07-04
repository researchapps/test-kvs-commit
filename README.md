# 🦩️ Test KVS Commit 🦩️

Build the container - this will use the flux-sched base and add our tests,
and then we can easily run them in one swoop!

```bash
$ docker build -t flamingo-mamma .
```

And then run the tests. This will:

1. Launch a job that asks for more resources than we have, flagged as burstable, but with urgency 0 so it stays in state `SCHED`
3. Run tests to try changing the kvs, either the jobspec or an attribute directory

Both tests will fail.

```bash
$ docker run -it flamingo-mamma flux start --test-size=4 /code/run_tests.sh
```

Here is the output (without pytest traceback) that shows the failures - I've separated
them into sections for easier readability.

```console
Submitting job...
flux submit -N 6 --urgency=0 --setattr=burstable hostname
ƒVXXBVq
```
```console
Is the job scheduled?
       JOBID USER     NAME       ST NTASKS NNODES     TIME INFO
     ƒVXXBVq fluxuser hostname    S      6      6        - 

```
```console
Running tests now (warning, they both fail)!
======================================== test session starts ========================================
platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0
rootdir: /code
collected 1 item                                                                                    

test_flux.py 
==== TESTING ADDING AN ATTRIBUTE TO KVS

Found jobs:
{
    "jobs": [
        {
            "id": 18723373056,
            "userid": 1002,
            "urgency": 0,
            "priority": 0,
            "t_submit": 1688429139.2131276,
            "t_depend": 1688429139.2246783,
            "state": 8,
            "name": "hostname",
            "cwd": "/code",
            "ntasks": 6,
            "duration": 0.0,
            "nnodes": 6
        }
    ]
}

🧝‍♀️️ Adding a new variable to the kvs and committing!
Found value None
🦾️ Re-retrieving the kvs...
🧐️ Is burstable there?
Found value None
F

============================================= FAILURES ==============================================
_______________________________________ test_adding_attribute _______________________________________

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
>       assert kvs.get("burstable")
E       AssertionError: assert None
E        +  where None = <bound method Mapping.get of <flux.kvs.KVSDir object at 0x7f73d6efda60>>('burstable')
E        +    where <bound method Mapping.get of <flux.kvs.KVSDir object at 0x7f73d6efda60>> = <flux.kvs.KVSDir object at 0x7f73d6efda60>.get

test_flux.py:76: AssertionError
========================================= warnings summary ==========================================
../home/fluxuser/.local/lib/python3.8/site-packages/_pytest/cacheprovider.py:451
  /home/fluxuser/.local/lib/python3.8/site-packages/_pytest/cacheprovider.py:451: PytestCacheWarning: cache could not write path /code/.pytest_cache/v/cache/nodeids: [Errno 13] Permission denied: '/code/.pytest_cache/v/cache/nodeids'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

../home/fluxuser/.local/lib/python3.8/site-packages/_pytest/stepwise.py:56
  /home/fluxuser/.local/lib/python3.8/site-packages/_pytest/stepwise.py:56: PytestCacheWarning: cache could not write path /code/.pytest_cache/v/cache/stepwise: [Errno 13] Permission denied: '/code/.pytest_cache/v/cache/stepwise'
    session.config.cache.set(STEPWISE_CACHE_DIR, [])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
====================================== short test summary info ======================================
FAILED test_flux.py::test_adding_attribute - AssertionError: assert None
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=================================== 1 failed, 2 warnings in 0.11s ===================================
😭️
```
```console
======================================== test session starts ========================================
platform linux -- Python 3.8.10, pytest-7.4.0, pluggy-1.2.0
rootdir: /code
collected 1 item                                                                                    

test_flux.py 
==== TESTING UPDATING A JOBSPEC

Found jobs:
{
    "jobs": [
        {
            "id": 18723373056,
            "userid": 1002,
            "urgency": 0,
            "priority": 0,
            "t_submit": 1688429139.2131276,
            "t_depend": 1688429139.2246783,
            "state": 8,
            "name": "hostname",
            "cwd": "/code",
            "ntasks": 6,
            "duration": 0.0,
            "nnodes": 6
        }
    ]
}

🦊️ Initial jobspec
{
    "resources": [
        {
            "type": "node",
            "count": 6,
            "exclusive": true,
            "with": [
                {
                    "type": "slot",
                    "count": 1,
                    "with": [
                        {
                            "type": "core",
                            "count": 1
                        }
                    ],
                    "label": "task"
                }
            ]
        }
    ],
    "tasks": [
        {
            "command": [
                "hostname"
            ],
            "slot": "task",
            "count": {
                "per_slot": 1
            }
        }
    ],
    "attributes": {
        "system": {
            "duration": 0,
            "cwd": "/code",
            "shell": {
                "options": {
                    "rlimit": {
                        "cpu": -1,
                        "fsize": -1,
                        "data": -1,
                        "stack": 8388608,
                        "core": -1,
                        "nofile": 1048576,
                        "as": -1,
                        "rss": -1,
                        "nproc": -1
                    }
                }
            },
            "burstable": 1
        }
    },
    "version": 1
}

🤪️ Removing burstable...

🧐️ Confirm it's not there!
{
    "resources": [
        {
            "type": "node",
            "count": 6,
            "exclusive": true,
            "with": [
                {
                    "type": "slot",
                    "count": 1,
                    "with": [
                        {
                            "type": "core",
                            "count": 1
                        }
                    ],
                    "label": "task"
                }
            ]
        }
    ],
    "tasks": [
        {
            "command": [
                "hostname"
            ],
            "slot": "task",
            "count": {
                "per_slot": 1
            }
        }
    ],
    "attributes": {
        "system": {
            "duration": 0,
            "cwd": "/code",
            "shell": {
                "options": {
                    "rlimit": {
                        "cpu": -1,
                        "fsize": -1,
                        "data": -1,
                        "stack": 8388608,
                        "core": -1,
                        "nofile": 1048576,
                        "as": -1,
                        "rss": -1,
                        "nproc": -1
                    }
                }
            }
        }
    },
    "version": 1
}

🧝‍♀️️ Updating the spec in kvs and committing!
🦾️ Re-retrieving the kvs and spec...
🧐️ Is burstable there?
{
    "resources": [
        {
            "type": "node",
            "count": 6,
            "exclusive": true,
            "with": [
                {
                    "type": "slot",
                    "count": 1,
                    "with": [
                        {
                            "type": "core",
                            "count": 1
                        }
                    ],
                    "label": "task"
                }
            ]
        }
    ],
    "tasks": [
        {
            "command": [
                "hostname"
            ],
            "slot": "task",
            "count": {
                "per_slot": 1
            }
        }
    ],
    "attributes": {
        "system": {
            "duration": 0,
            "cwd": "/code",
            "shell": {
                "options": {
                    "rlimit": {
                        "cpu": -1,
                        "fsize": -1,
                        "data": -1,
                        "stack": 8388608,
                        "core": -1,
                        "nofile": 1048576,
                        "as": -1,
                        "rss": -1,
                        "nproc": -1
                    }
                }
            },
            "burstable": 1
        }
    },
    "version": 1
}
F

============================================= FAILURES ==============================================
__________________________________________ test_kvs_commit __________________________________________

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
>       assert "burstable" not in spec["attributes"]["system"]
E       AssertionError: assert 'burstable' not in {'burstable': 1, 'cwd': '/code', 'duration': 0, 'shell': {'options': {'rlimit': {'as': -1, 'core': -1, 'cpu': -1, 'data': -1, ...}}}}

test_flux.py:47: AssertionError
========================================= warnings summary ==========================================
../home/fluxuser/.local/lib/python3.8/site-packages/_pytest/cacheprovider.py:451
  /home/fluxuser/.local/lib/python3.8/site-packages/_pytest/cacheprovider.py:451: PytestCacheWarning: cache could not write path /code/.pytest_cache/v/cache/nodeids: [Errno 13] Permission denied: '/code/.pytest_cache/v/cache/nodeids'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

../home/fluxuser/.local/lib/python3.8/site-packages/_pytest/stepwise.py:56
  /home/fluxuser/.local/lib/python3.8/site-packages/_pytest/stepwise.py:56: PytestCacheWarning: cache could not write path /code/.pytest_cache/v/cache/stepwise: [Errno 13] Permission denied: '/code/.pytest_cache/v/cache/stepwise'
    session.config.cache.set(STEPWISE_CACHE_DIR, [])

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
====================================== short test summary info ======================================
FAILED test_flux.py::test_kvs_commit - AssertionError: assert 'burstable' not in {'burstable': 1, 'cwd': '/code', 'duration': 0, 'shell...
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=================================== 1 failed, 2 warnings in 0.11s ===================================
😭️
🍴️ Stick a fork in me, I'm done.
```

That second one is more interesting because even the kvs.get (before we instantiate again)
does not work.
