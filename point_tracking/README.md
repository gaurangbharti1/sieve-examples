# Point Tracking

Tracks a point through a video using a Kanade-Lucas-Tomasi (KLT) tracker.

## Deploying

Follow our [getting started guide](https://docs.sievedata.com/guide/quickstart/custom-workflows) to get your Sieve API key and install the Sieve Python client.

1. Export API keys & install Python client

```
export SIEVE_API_KEY={YOUR_API_KEY}
pip install https://mango.sievedata.com/v1/client_package/sievedata-0.0.1.1.2-py3-none-any.whl
```

2. Deploy a workflow to Sieve

```
git clone git@github.com:sieve-community/examples.git
cd examples/point_tracking
sieve deploy
```