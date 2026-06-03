from flask import Blueprint, jsonify, render_template_string

from app.controllers.home_controller import get_system_status, get_status_json

home_bp = Blueprint("home", __name__)

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SkinSense AI — API</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
  .container { max-width: 900px; margin: 0 auto; padding: 40px 24px; }
  h1 { font-size: 28px; font-weight: 700; margin-bottom: 4px; }
  h1 span { color: #38bdf8; }
  .subtitle { color: #94a3b8; font-size: 14px; margin-bottom: 32px; }

  .card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; margin-bottom: 20px; }
  .card h2 { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: #f1f5f9; }

  .status-row { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid #334155; }
  .status-row:last-child { border-bottom: none; }
  .dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .dot.ok { background: #22c55e; box-shadow: 0 0 6px #22c55e88; }
  .dot.err { background: #ef4444; box-shadow: 0 0 6px #ef444488; }
  .status-label { font-size: 14px; color: #cbd5e1; }
  .status-value { margin-left: auto; font-size: 13px; color: #94a3b8; font-family: 'SF Mono', 'Cascadia Code', monospace; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 340px; }

  .endpoint-group { margin-bottom: 20px; }
  .endpoint-group:last-child { margin-bottom: 0; }
  .endpoint-group h3 { font-size: 13px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }

  .endpoint { display: flex; align-items: flex-start; gap: 10px; padding: 12px 14px; background: #0f172a; border-radius: 8px; margin-bottom: 8px; }
  .method { font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; font-family: monospace; flex-shrink: 0; min-width: 52px; text-align: center; margin-top: 2px; }
  .method.post { background: #164e63; color: #22d3ee; }
  .method.get { background: #14532d; color: #4ade80; }
  .ep-body { flex: 1; min-width: 0; }
  .path { font-size: 14px; font-family: 'SF Mono', 'Cascadia Code', monospace; color: #e2e8f0; }
  .desc { font-size: 12px; color: #64748b; margin-top: 3px; }

  .tag { display: inline-block; font-size: 10px; padding: 2px 6px; border-radius: 3px; margin-left: 8px; font-weight: 600; vertical-align: middle; }
  .tag.auth { background: #7c3aed22; color: #a78bfa; border: 1px solid #7c3aed44; }
  .tag.public { background: #0d946822; color: #2dd4bf; border: 1px solid #0d946844; }

  .payload { margin-top: 10px; }
  .payload summary { font-size: 12px; cursor: pointer; user-select: none; padding: 4px 0; }
  .payload summary:hover { color: #e2e8f0; }
  .payload summary.req { color: #22d3ee; }
  .payload summary.res { color: #4ade80; }
  .payload summary.err { color: #fb923c; }
  .payload pre { margin-top: 6px; background: #020617; padding: 12px; border-radius: 6px; font-size: 12px; color: #94a3b8; overflow-x: auto; line-height: 1.5; border: 1px solid #1e293b; }
  .payload .status-code { font-size: 11px; color: #64748b; margin-left: 6px; }

  .ref-pre { background: #0f172a; padding: 12px; border-radius: 6px; font-size: 12px; color: #94a3b8; line-height: 1.6; overflow-x: auto; }

  footer { text-align: center; color: #475569; font-size: 12px; margin-top: 32px; }
</style>
</head>
<body>
<div class="container">
  <h1>SkinSense <span>AI</span></h1>
  <p class="subtitle">Backend API — PJK-GM066</p>

  <div class="card">
    <h2>System Status</h2>
    <div class="status-row">
      <div class="dot {{ 'ok' if model_loaded else 'err' }}"></div>
      <span class="status-label">ML Model (SkincareRecommender)</span>
      <span class="status-value">{{ product_count }} products loaded</span>
    </div>
    <div class="status-row">
      <div class="dot {{ 'ok' if model_loaded else 'err' }}"></div>
      <span class="status-label">ML Model Path</span>
      <span class="status-value" title="{{ ml_path }}">{{ ml_path }}</span>
    </div>
    <div class="status-row">
      <div class="dot {{ 'ok' if db_ok else 'err' }}"></div>
      <span class="status-label">Database</span>
      <span class="status-value">{{ db_status }}</span>
    </div>
    <div class="status-row">
      <div class="dot {{ 'ok' if weather_key else 'err' }}"></div>
      <span class="status-label">WeatherAPI Key</span>
      <span class="status-value">{{ 'configured' if weather_key else 'not set — add WEATHERAPI_KEY to .env' }}</span>
    </div>
    <div class="status-row">
      <div class="dot ok"></div>
      <span class="status-label">Server Time</span>
      <span class="status-value">{{ server_time }}</span>
    </div>
  </div>

  <div class="card">
    <h2>API Documentation</h2>

    <div class="endpoint-group">
      <h3>Authentication</h3>

      <div class="endpoint">
        <span class="method post">POST</span>
        <div class="ep-body">
          <div class="path">/api/auth/register <span class="tag public">public</span></div>
          <div class="desc">Register a new user account</div>
          <details class="payload">
            <summary class="req">Request body</summary>
            <pre>{
  "email": "user@example.com",
  "password": "min6chars",
  "name": "User Name"
}</pre>
          </details>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">201</span></summary>
            <pre>{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}</pre>
          </details>
          <details class="payload">
            <summary class="err">Error responses</summary>
            <pre>400  { "error": "Email and password are required" }
400  { "error": "Password must be at least 6 characters" }
409  { "error": "Email already registered" }</pre>
          </details>
        </div>
      </div>

      <div class="endpoint">
        <span class="method post">POST</span>
        <div class="ep-body">
          <div class="path">/api/auth/login <span class="tag public">public</span></div>
          <div class="desc">Login and receive JWT token</div>
          <details class="payload">
            <summary class="req">Request body</summary>
            <pre>{
  "email": "user@example.com",
  "password": "yourpassword"
}</pre>
          </details>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">200</span></summary>
            <pre>{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}</pre>
          </details>
          <details class="payload">
            <summary class="err">Error responses</summary>
            <pre>400  { "error": "Email and password are required" }
401  { "error": "Invalid email or password" }</pre>
          </details>
        </div>
      </div>

      <div class="endpoint">
        <span class="method post">POST</span>
        <div class="ep-body">
          <div class="path">/api/auth/guest <span class="tag public">public</span></div>
          <div class="desc">Create a guest session (no registration needed)</div>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">201</span></summary>
            <pre>{
  "user_id": "f8e7d6c5-...",
  "session_token": "b3a4c5d6-...",
  "expires_at": "2026-06-04T11:30:00+00:00"
}</pre>
          </details>
        </div>
      </div>

      <div class="endpoint">
        <span class="method get">GET</span>
        <div class="ep-body">
          <div class="path">/api/auth/me <span class="tag auth">JWT</span></div>
          <div class="desc">Get current user info. Header: <code style="color:#94a3b8;">Authorization: Bearer &lt;token&gt;</code></div>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">200</span></summary>
            <pre>{
  "user_id": "a1b2c3d4-...",
  "email": "user@example.com",
  "name": "User Name",
  "is_guest": false
}</pre>
          </details>
          <details class="payload">
            <summary class="err">Error responses</summary>
            <pre>401  { "error": "Authorization header required" }
401  { "error": "Invalid or expired token" }
404  { "error": "User not found" }</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="endpoint-group">
      <h3>Recommendation</h3>

      <div class="endpoint">
        <span class="method post">POST</span>
        <div class="ep-body">
          <div class="path">/api/recommend <span class="tag public">public</span></div>
          <div class="desc">Submit skin profile + location &rarr; get personalized product recommendations</div>
          <details class="payload">
            <summary class="req">Request body</summary>
            <pre>{
  "user_id": "uuid-or-null",
  "session_token": "string-for-guest",
  "questionnaire": {
    "product_category": "sunscreen",
    "skin_type": "oily",
    "skin_concerns": ["acne", "dullness"],
    "activity_type": "outdoor",
    "avoided_ingredients": ["retinol"]
  },
  "location": {
    "lat": -6.2088,
    "lon": 106.8456,
    "method": "gps"
  }
}</pre>
          </details>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">200</span></summary>
            <pre>{
  "questionnaire_id": "e1f2a3b4-...",
  "weather": {
    "temperature": 34.2,
    "humidity": 78,
    "uv_index": 9.0,
    "pm25": 38.4
  },
  "recommendations": [
    {
      "rank": 1,
      "product_name": "UV Perfect Aqua Essence",
      "brand": "L'OREAL",
      "category": "sunscreen",
      "skin_types": ["oily", "combination"],
      "active_ingredients": ["niacinamide", "zinc oxide"],
      "why_recommended": "Cocok karena sangat cocok untuk tipe kulit oily...",
      "score": 0.87
    }
  ]
}</pre>
          </details>
          <details class="payload">
            <summary class="err">Error responses</summary>
            <pre>400  { "error": "Invalid product_category. Must be one of: ..." }
400  { "error": "Invalid skin_type. Must be one of: ..." }
400  { "error": "Location (lat, lon) is required" }
502  { "error": "Failed to fetch weather data: ..." }</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="endpoint-group">
      <h3>History</h3>

      <div class="endpoint">
        <span class="method get">GET</span>
        <div class="ep-body">
          <div class="path">/api/history <span class="tag auth">JWT</span></div>
          <div class="desc">Get recommendation history. Header: <code style="color:#94a3b8;">Authorization: Bearer &lt;token&gt;</code></div>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">200</span></summary>
            <pre>{
  "history": [
    {
      "questionnaire_id": "e1f2a3b4-...",
      "product_category": "sunscreen",
      "skin_type": "oily",
      "skin_concerns": ["acne", "dullness"],
      "activity_type": "outdoor",
      "avoided_ingredients": ["retinol"],
      "location": { "lat": -6.2088, "lon": 106.8456, "method": "gps" },
      "created_at": "2026-06-03T10:30:00",
      "weather": { "temperature": 34.2, "humidity": 78, "uv_index": 9.0, "pm25": 38.4 },
      "recommendations": [
        {
          "rank": 1,
          "product_name": "UV Perfect Aqua Essence",
          "brand": "L'OREAL",
          "category": "sunscreen",
          "score": 0.87
        }
      ]
    }
  ]
}</pre>
          </details>
          <details class="payload">
            <summary class="err">Error responses</summary>
            <pre>401  { "error": "Authorization header required" }
401  { "error": "Invalid or expired token" }</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="endpoint-group">
      <h3>Health Check</h3>

      <div class="endpoint">
        <span class="method get">GET</span>
        <div class="ep-body">
          <div class="path">/api/status <span class="tag public">public</span></div>
          <div class="desc">JSON health check for monitoring</div>
          <details class="payload">
            <summary class="res">Expected response <span class="status-code">200</span></summary>
            <pre>{
  "status": "ok",
  "model_loaded": true,
  "product_count": 1472,
  "database": true,
  "weather_api_configured": true,
  "ml_model_path": "/path/to/machine-learning",
  "server_time": "2026-06-03T11:30:00+00:00"
}</pre>
          </details>
        </div>
      </div>
    </div>

    <div class="endpoint-group">
      <h3>Reference Values</h3>
      <div class="endpoint" style="display:block;">
        <div class="desc" style="margin-bottom:8px;">Valid values for questionnaire fields:</div>
        <pre class="ref-pre">product_category : moisturizer | cleanser | face mask | eye cream | sunscreen
skin_type        : normal | dry | oily | combination | sensitive
skin_concerns    : acne | dullness | aging | dark spots | dehydration
activity_type    : indoor | outdoor  (only when product_category = sunscreen)
location method  : gps | manual_map</pre>
      </div>
    </div>
  </div>

  <footer>SkinSense AI &middot; Capstone Pijak &times; IBM SkillsBuild &middot; PJK-GM066</footer>
</div>
</body>
</html>
"""


@home_bp.route("/")
def home():
    status = get_system_status()
    return render_template_string(HOME_HTML, **status)


@home_bp.route("/api/status")
def status_json():
    result, status_code = get_status_json()
    return jsonify(result), status_code
