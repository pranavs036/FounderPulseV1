// MongoDB initialization script
db = db.getSiblingDB('growth_copilot_db');

// Create collections
db.createCollection('mixpanel_data');
db.createCollection('moengage_data');
db.createCollection('jira_data');
db.createCollection('anomalies');
db.createCollection('insights');
db.createCollection('action_logs');

// Create indexes for better performance
db.mixpanel_data.createIndex({ "date": 1, "metric": 1 });
db.anomalies.createIndex({ "metric": 1, "platform": 1 });
db.insights.createIndex({ "anomaly_id": 1 });
db.action_logs.createIndex({ "timestamp": -1 });

print('MongoDB initialization completed');
