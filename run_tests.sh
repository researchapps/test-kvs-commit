#!/bin/bash

echo "Submitting job..."
echo "flux submit -N 6 --urgency=0 --setattr=burstable hostname"
flux submit -N 6 --urgency=0 --setattr=burstable hostname

echo "Is the job scheduled?"
flux jobs -a

echo "Running tests now (warning, they both fail)!"

pytest -xs test_flux.py::test_adding_attribute || echo "😭️"
pytest -xs test_flux.py::test_kvs_commit  || echo "😭️"

echo "🍴️ Stick a fork in me, I'm done."
