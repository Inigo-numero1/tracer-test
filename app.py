import argparse
import random
import time

from flask import Flask, redirect, url_for


# [START trace_setup_python_configure]
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
import opencensus.trace.tracer


def initialize_tracer(project_id):
    exporter = stackdriver_exporter.StackdriverExporter(
        project_id=project_id
    )
    tracer = opencensus.trace.tracer.Tracer(
        exporter=exporter,
        sampler=opencensus.trace.tracer.samplers.AlwaysOnSampler()
    )

    return tracer
# [END trace_setup_python_configure]


app = Flask(__name__)

tracer = initialize_tracer('itranslate-translate')
app.config['TRACER'] = tracer


@app.route('/healthz', methods=['GET'])
def root():
    return 'OK'


# [START trace_setup_python_quickstart]
@app.route('/index', methods=['GET'])
def index():
    tracer = app.config['TRACER']
    tracer.start_span(name='index')

    result = "Tracing requests"

    tracer.end_span()
    return result
# [END trace_setup_python_quickstart]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--project_id', help='itranslate-translate', required=True)
    args = parser.parse_args()

    # tracer = initialize_tracer(args.project_id)
    # app.config['TRACER'] = tracer

    app.run()