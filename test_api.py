import requests
import json

try:
    response = requests.get('http://localhost:5000/api/statistics')
    data = response.json()
    
    print("✅ Respuesta de /api/statistics:")
    print(json.dumps(data, indent=2))
    
    if data.get('success') and data.get('data'):
        print("\n📊 Resumen de totales:")
        for item in data['data']:
            print(f"  • {item['metric_name']}: {item.get('total_value', 'N/A'):,}")
    
except Exception as e:
    print(f"❌ Error: {e}")
