
# I wrote this using ChatGPT
#========== context propagation  import the necessary libraries 
from opentelemetry import trace, baggage
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.baggage.propagation import W3CBaggagePropagator
#========== for redis spans
from opentelemetry.instrumentation.redis import RedisInstrumentor
#==========
from flask import Flask, jsonify, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics
from flask_cors import CORS
import redis, os, time
import psutil

#========== context propagation  set up the OpenTelemetry SDK
trace.set_tracer_provider(TracerProvider())
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
tracer = trace.get_tracer(__name__)
#==========
#========== Instrument Redis
RedisInstrumentor().instrument()

#========== context propagation function to extract the trace context from the request headers:
def extract_trace_context(headers):
    carrier = {'traceparent': headers.get('Traceparent', '')}
    ctx = TraceContextTextMapPropagator().extract(carrier=carrier)
    b2 = {'baggage': headers.get('Baggage', '')}
    ctx2 = W3CBaggagePropagator().extract(b2, context=ctx)
    return ctx2
#========== context propagation functionto inject the trace context into the response headers:
def inject_trace_context(headers, ctx):
    W3CBaggagePropagator().inject(headers, ctx)
    TraceContextTextMapPropagator().inject(headers, ctx)
#==========

# token = "djuadsuhfoiurnvaiusndvoan"
app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"])
CORS(app)

metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.0')

redis_password = os.getenv("REDIS_PASSWORD","12345")
host=os.getenv("REDIS_HOST","localhost")
port=os.getenv("REDIS_PORT","6379")

r = redis.Redis(host=host, 
                port=port,
                password=redis_password,
                db=0)

# Create gauges for memory and CPU usage
memory_usage_gauge = Gauge('memory_usage_bytes', 'Memory usage in bytes')
cpu_usage_gauge = Gauge('cpu_usage_percent', 'CPU usage percent')

@app.route('/', methods=['GET'])
def index():
    # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("index_span", context=ctx):
      # Perform the API logic
      # Get all engineer names and skills from the Redis database
      engineer_data = {}
      for key in r.scan_iter():
          engineer_data[key.decode()] = r.get(key).decode()
      
      # Return a welcome message and the list of engineers, or an error message if there are ====
      # =no engineers
  
      if len(engineer_data) == 0:
          return '<h3>Welcome to Skillsets! No engineers with skillsets to display.</h3> <p>Please add your first engineer by running "curl -X POST -H "Content-Type: application/json" -d \'{\"name\": \"Alice\", \"skills\": \"Python, SQL, Flask\"}\' http://HOST:5000/add_engineer".</p>'
      else:
          return f'<h2>Welcome to Skillsets!</h2> \n {engineer_data}'


@app.route('/healthz')
def welcome():
    return "<h2>100% Healthy!</h1>"

@app.route('/add_engineer', methods=['POST'])
def add_engineer():
    # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("add new engineer", context=ctx):
      # Get the engineer data from the request body
      engineer_data = request.json
      
      # Validate the engineer data format
      if 'name' not in engineer_data or 'skills' not in engineer_data:
          return jsonify({'error': 'Invalid engineer data format'}), 400
      
      # Check if the engineer name already exists in the database
      if r.exists(engineer_data['name']):
          # Return an error message if the name already exists
          return jsonify({'error': 'Engineer name already exists'}), 409 # Conflict
      
      # Add the engineer to the Redis database
      r.set(engineer_data['name'], engineer_data['skills'])
  
      # Return a success message
      return jsonify({'message': 'Engineer added successfully'}), 200


@app.route('/update_engineer_skillset/<engineer_name>', methods=['PUT'])
def update_engineer_skillset(engineer_name):
        # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("update engineer skills", context=ctx):
      # Get the new skill set from the request body
      new_skill_set = request.get_json().get('skills')
      
      # Check if the engineer name exists in the Redis database
      if not r.exists(engineer_name):
          return jsonify({'message': 'Engineer name not found'}), 404
      
      # Update the skill set in the Redis database
      r.set(engineer_name, new_skill_set)
      
      # Return a success message
      return jsonify({'message': 'Skillset updated successfully'}), 200

@app.route('/get_skills', methods=['GET'])
def get_skills():
        # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("list skills", context=ctx):
      # Get the name of the engineer to retrieve skills for from the query string
      name = request.args.get('name')
      
      # Retrieve the engineer's skills from the Redis database
      skills = r.get(name)
      
      # Return the skills as a JSON response
      return jsonify({'skills': skills.decode()})

@app.route('/get_engineers_by_skill/<skill>', methods=['GET'])
def get_engineers_by_skill(skill):
        # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("get engineers by skill", context=ctx):
      # Get all engineer names and skills from the Redis database
      engineer_data = {}
      for key in r.scan_iter():
          engineer_data[key.decode()] = r.get(key).decode()
      
      # Filter engineer names by skill
      filtered_names = [name for name, skills in engineer_data.items() if skill in skills]
      
      # Return the filtered engineer names as a JSON response, or an error message if there are no matching engineers
      if len(filtered_names) == 0:
          return jsonify({'error': f'No engineer found with the skillset {skill}.'})
      else:
          return jsonify({'engineers': filtered_names})


@app.route('/get_all_engineers', methods=['GET'])
def get_all_engineers():
        # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("get all engineers", context=ctx):
      # Get all engineer names and skills from the Redis database
      engineer_data = {}
      for key in r.scan_iter():
          engineer_data[key.decode()] = r.get(key).decode()
      # Return the engineer data as a JSON response
      return jsonify(engineer_data)

## New line ## NOT JSON
@app.route('/get_all_engineers_new', methods=['GET'])
def get_all_engineers_new():
        # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("get all engineers new format", context=ctx):
      # Get all engineer names and skills from the Redis database
      engineer_data = {}
      for key in r.scan_iter():
          engineer_data[key.decode()] = r.get(key).decode()
      
      # Format the engineer data as a string with each engineer on a new line
      formatted_engineer_data = '\n'.join([f'{k}: {v}' for k, v in engineer_data.items()])
      
      # Return the formatted engineer data as a string
      return formatted_engineer_data


@app.route('/delete_engineer/<engineer_name>', methods=['DELETE'])
def delete_engineer(engineer_name):
        # Extract the trace context from the request headers
    ctx = extract_trace_context(request.headers)

    # Start a new span for this route handler
    with tracer.start_as_current_span("delete engineer by name", context=ctx):
      # Check if the engineer exists in the Redis database
      if not r.exists(engineer_name):
          return f"Engineer with name '{engineer_name}' does not exist", 404
      # Delete the engineer from the Redis database
      r.delete(engineer_name)
      # Return a success message
      return f"Engineer with name '{engineer_name}' has been deleted",  200

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False) # Bandit -  Severity: High   Confidence: Medium
    app.run()