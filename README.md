# Database Ingestion for Data Lakes

A Data Lake ingestion connector for databases

The main component of the repository is an AWS Glue job, of type `pythonshell`, which uses a glue connection and AWS Wrangler to make the parquet version of the extracted data.

The infrastructure is described (IaC) and deployed with Serverless Framework (https://www.serverless.com/framework/). The entry point is `rds-ingest/serverless.yml`.

The infrastructure has been developed on the AWS Cloud Platform.

## Getting Started

### Requirements

- Node.js and NPM: https://nodejs.org/en/download/
- Serverless Framework: https://www.serverless.com/framework/docs/getting-started/

#### For local development only

- Python: https://www.python.org/downloads/
- virtualenv: https://virtualenv.pypa.io/en/latest/installation.html

### Environments setup

The `rds-ingest/env/` contains the environment configuration files, one for each of your AWS environments.

The name of the files corresponds to the environment names. For example: substitute `example_enviroment.yml` with `dev.yml` for a development environment.

### Development environment setup

1. Create virtualenv: `virtualenv -p python3 venv`
2. Activate virtualenv: `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`

### Deployment instructions

1. You need two AWS S3 buckets, one for the glue code and one as the Data Lake, if you have them, just keep in mind the names for the nexts steps, otherwise create the buckets on S3.

2. Make a copy of `rds-ingest/env/example-environment.yml`, name it as your desired environment's name (for example `dev.yml` or `prod.yml`) and substitute:

   - `example-data-s3-bucket-name` for your data lake AWS S3 bucket.
   - `example-code-s3-bucket-name` for your code AWS S3 bucket.
   - `eu-west-1` with your AWS region.

3. Make a Glue Connection to your RDS instance and test if it works.

   - For example, we named it `test-connection`.

4.  Deploy on AWS with: `sls deploy --stage {stage}`.
   1. Substitute `{stage}` with one of the available stages defined as the YAML files in the `rds-ingest/env/` directory.



## Contributing

Feel free to contribute! Create an issue and submit PRs (pull requests) in the repository. Contributing to this project assumes a certain level of familiarity with AWS, the Python language and concepts such as virtualenvs, pip, modules, etc.

Try to keep commits inside the rules of https://www.conventionalcommits.org/. The `sailr.json` file is used for configuration of the commit hook, as per: https://github.com/craicoverflow/sailr.

## License

This project is licensed under the **Apache License 2.0**.

See [LICENSE](LICENSE) for more information.

## Acknowledgements

Many thanks to the mantainers of the open source libraries used in this project:

- Serverless Framework: https://github.com/serverless/serverless
- Pandas: https://github.com/pandas-dev/pandas
- AWS Data Wrangler: https://github.com/awslabs/aws-data-wrangler
- Boto3 (AWS SDK for Python): https://github.com/boto/boto3
- Sailr (conventional commits git hooke): https://github.com/craicoverflow/sailr/

### Serverless plugins

These are the Serverless plugin used on this project:

- serverless-step-functions: https://github.com/serverless-operations/serverless-step-functions
- serverless-plugin-log-retention: https://github.com/ArtificerEntertainment/serverless-plugin-log-retention
- serverless-glue: https://github.com/toryas/serverless-glue
- serverless-s3-sync: https://github.com/k1LoW/serverless-s3-sync

Contact us if we missed an acknowledgement to your library.

---

This is a project created by [Linkalab](https://linkalab.it) and [Talent Garden](https://talentgarden.org).
