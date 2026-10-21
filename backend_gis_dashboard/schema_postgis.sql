CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS ward_boundary (
    ward_id SERIAL PRIMARY KEY,
    ward_code TEXT UNIQUE NOT NULL,
    ward_name TEXT NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incident_event (
    incident_id BIGSERIAL PRIMARY KEY,
    source_channel TEXT NOT NULL CHECK (source_channel IN ('rover', 'citizen_app', 'web', 'voice')),
    category TEXT NOT NULL CHECK (category IN ('Emergency', 'Municipal')),
    subtype TEXT,
    description TEXT,
    severity SMALLINT NOT NULL CHECK (severity BETWEEN 1 AND 10),
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'escalated')),
    geo GEOGRAPHY(Point, 4326) NOT NULL,
    ward_code TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_incident_event_geo ON incident_event USING GIST (geo);
CREATE INDEX IF NOT EXISTS idx_incident_event_category_status ON incident_event (category, status);
CREATE INDEX IF NOT EXISTS idx_incident_event_severity ON incident_event (severity DESC);

CREATE TABLE IF NOT EXISTS incident_resolution_feedback (
    feedback_id BIGSERIAL PRIMARY KEY,
    incident_id BIGINT NOT NULL REFERENCES incident_event(incident_id) ON DELETE CASCADE,
    resolver_agency TEXT NOT NULL,
    resolution_note TEXT,
    citizen_rating SMALLINT CHECK (citizen_rating BETWEEN 1 AND 5),
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE VIEW ward_sustainability_heatmap AS
SELECT
    i.ward_code,
    COUNT(*) AS total_incidents,
    AVG(i.severity)::NUMERIC(4,2) AS avg_severity,
    SUM(CASE WHEN i.category = 'Municipal' THEN 1 ELSE 0 END) AS municipal_count,
    SUM(CASE WHEN i.category = 'Emergency' THEN 1 ELSE 0 END) AS emergency_count
FROM incident_event i
GROUP BY i.ward_code;
