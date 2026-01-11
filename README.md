
# 🎨 TrueShade Backend

**Scientific skin tone analysis and makeup shade matching using computer vision and color science**

TrueShade is an AI-powered backend system that analyzes facial images to determine precise skin tone and recommend perfectly matched makeup shades from real beauty brands.

> **⚠️ Python Version Requirement**: This project requires **Python 3.12** due to MediaPipe compatibility. Python 3.13+ is not yet supported by MediaPipe.

## 🔬 How It Works

1. **Face Detection**: MediaPipe Face Mesh detects 478 facial landmarks
2. **Skin Extraction**: Isolates pure skin regions (cheeks, forehead, jaw)
3. **Color Analysis**: Converts pixels to LAB color space
4. **K-Means Clustering**: Finds dominant skin tone
5. **Shade Matching**: Compares to 89 real makeup products using Delta E (ΔE) color distance
6. **Recommendations**: Returns best matches from Fenty Beauty, NARS, and Too Faced

## 🏗️ Architecture

```
TrueShade Backend
│
├── Face Detection Layer (MediaPipe)
│   └── Extracts facial landmarks and skin regions
│
├── Color Analysis Layer (OpenCV + scikit-learn)
│   └── LAB color space conversion + K-Means clustering
│
├── Shade Matching Layer (Supabase + Delta E)
│   └── Database queries + color distance calculation
│
└── REST API (FastAPI)
    └── JSON responses for frontend
```

## 📁 Project Structure

```
TrueColor/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── models/
│   │   └── response_models.py     # Pydantic response schemas
│   ├── services/
│   │   ├── face_detection.py      # MediaPipe face detection
│   │   ├── skin_analysis.py       # LAB color analysis & K-Means
│   │   └── shade_matcher.py       # Makeup shade matching
│   ├── database/
│   │   └── supabase_client.py     # Supabase integration
│   ├── data/
│   │   └── makeup_database.py     # Fallback product database
│   └── utils/
│       └── image_utils.py         # Image preprocessing
├── database/
│   ├── schema.sql                 # Supabase database schema
│   ├── seed.py                    # Database seeding script
│   └── clear.py                   # Database cleanup script
├── requirements.txt               # Python dependencies
├── run.py                         # Server entry point
├── test_api.py                    # API testing script
├── test_components.py             # Component status checker
├── test_supabase.py               # Supabase integration tests
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.12** (MediaPipe not compatible with 3.13+)
- **Supabase Account** (free tier works great)

### 1. Installation

```powershell
# Clone the repository
git clone https://github.com/yourusername/TrueColor.git
cd TrueColor

# Create virtual environment with Python 3.12
py -3.12 -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Supabase

1. Create a free account at [supabase.com](https://supabase.com)
2. Create a new project
3. Copy `.env.example` to `.env`
4. Add your Supabase credentials to `.env`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

5. Run the schema in Supabase SQL Editor:

```powershell
# Copy contents of database/schema.sql
# Paste into Supabase SQL Editor and run
```

6. Seed the database:

```powershell
python database/seed.py
```

### 3. Run the Server

```powershell
python run.py
```

The server will start at `http://localhost:8000`

### 4. Test the API

```powershell
# Check health
curl http://localhost:8000/health

# Test components
python test_components.py

# Test Supabase integration
python test_supabase.py

# Test with an image
python test_api.py path/to/face_image.jpg
```

### 5. View API Documentation

Open in browser: `http://localhost:8000/docs`

## 📡 API Endpoints

### POST `/analyze`

Analyzes a face image and returns skin tone + shade recommendations.

**Request:**
```http
POST /analyze
Content-Type: multipart/form-data

file: <image_file>
```

**Response:**
```json
{
  "skinLAB": [65.2, 12.4, 18.6],
  "undertone": "warm",
  "pantone_family": "4Y05",
  "fenty": ["310", "330", "340"],
  "nars": ["Barcelona", "Stromboli", "Syracuse"],
  "tooFaced": ["Warm Sand", "Golden Beige", "Honey"]
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "face_detection": "ready",
    "skin_analysis": "ready",
    "shade_matching": "ready"
  }
}
```

### POST `/analyze-debug`

Debug endpoint with detailed processing information.

## 🎯 Core Technologies

| Technology | Purpose |
|-----------|---------|
| **FastAPI** | REST API framework |
| **MediaPipe** | Face detection & landmark extraction (478 points) |
| **OpenCV** | Image processing & LAB color conversion |
| **scikit-learn** | K-Means clustering for dominant color |
| **NumPy** | Numerical computations |
| **Pydantic** | Data validation & schemas |
| **Supabase** | PostgreSQL database with real-time capabilities |
| **Python 3.12** | Required for MediaPipe compatibility |

## 🧪 LAB Color Space

TrueShade uses **LAB color space** instead of RGB because:

- **L** (Lightness): 0-100 (perceptually uniform)
- **A**: Green (-) to Red (+)
- **B**: Blue (-) to Yellow (+)

This allows **perceptually accurate** color matching using **Delta E (ΔE)** distance:

```
ΔE = √[(L₁-L₂)² + (A₁-A₂)² + (B₁-B₂)²]
```

**ΔE < 2**: Imperceptible difference  
**ΔE 2-5**: Small difference  
**ΔE 5-10**: Noticeable difference  

## 🎨 Undertone Detection

Based on **A** and **B** channels:

| Undertone | Criteria |
|-----------|----------|
| **Warm** | B > 15 and A > 8 (yellow-red) |
| **Cool** | B < 10 and A < 8 (blue-pink) |
| **Neutral** | Balanced A and B |

## 💄 Makeup Database

Current database includes **89 shades** from:

- **Fenty Beauty**: Pro Filt'r Foundation (45 shades)
- **NARS**: Natural Radiant Longwear (20 shades)
- **Too Faced**: Born This Way (24 shades)

Each shade stored with:
- Brand & product line name
- Shade name
- Hex color code
- **Precomputed LAB values** (L, A, B)
- Undertone classification (warm/cool/neutral)
- Timestamps (created_at, updated_at)

**Database Schema**:
- `makeup_products`: All product shades with LAB values
- `user_profiles`: User information and preferences
- `analysis_history`: Historical skin tone analyses
- `user_favorites`: User-favorited products

## 🔧 Configuration

Create `.env` file from template:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Never commit `.env` to version control!**

## 📊 Skin Region Extraction

MediaPipe Face Mesh provides 478 landmarks. We extract skin from:

- **Forehead**: Landmarks 10-67
- **Left Cheek**: Landmarks 123, 116, 117, etc.
- **Right Cheek**: Landmarks 352, 345, 346, etc.
- **Nose Bridge**: Landmarks 6, 168, 197, etc.
- **Chin**: Landmarks 152, 148, 176, etc.

## 🌈 Pantone SkinTone Approximation

Format: `[Depth][Undertone][Value]`

Example: **4Y05**
- **4**: Medium depth (1=lightest, 7=deepest)
- **Y**: Yellow undertone (Y/R/P/N)
- **05**: Value from A+B channels

## 🧩 Integration with Frontend

```javascript
// React/JavaScript example
const analyzeImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:8000/analyze', {
    method: 'POST',
    body: formData
  });
  
  const result = await response.json();
  console.log(result);
  // { skinLAB: [...], undertone: "warm", fenty: [...], ... }
};
```

## 🛠️ Development

### Run in Development Mode

```powershell
python run.py
# Auto-reload enabled in DEBUG mode
```

### Test Components

```powershell
# Check all component status
python test_components.py

# Test Supabase integration
python test_supabase.py

# Test API endpoint
python test_api.py test_image.jpg
```

### Database Management

```powershell
# Seed database with products
python database/seed.py

# Clear all products (careful!)
python database/clear.py

# Test database connection
python test_db.py
```

### Add New Brands

You can add products via Supabase dashboard or programmatically:

```python
from app.database.supabase_client import SupabaseClient

client = SupabaseClient(use_service_role=True)

new_product = {
    "brand": "Brand Name",
    "shade_name": "Shade Name",
    "hex_color": "#FFAA88",
    "lab_l": 65.2,
    "lab_a": 12.4,
    "lab_b": 18.6,
    "undertone": "warm"
}

await client.bulk_insert_products([new_product])
```

## � Production Deployment

### Environment Setup

1. **Set proper CORS origins** in `main.py`
2. **Use environment variables** for all secrets
3. **Enable Supabase Row Level Security (RLS)**
4. **Add rate limiting**
5. **Implement authentication** if needed

### Production Command

```bash
# Using Uvicorn with workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

### Deployment Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure CORS allowed origins
- [ ] Set up Supabase backups
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure logging
- [ ] Set resource limits
- [ ] Test with production data

## 🐛 Troubleshooting

### MediaPipe Not Working

**Problem**: `AttributeError: function 'free' not found`

**Solution**: You must use Python 3.12. MediaPipe is not compatible with Python 3.13+.

```powershell
# Install Python 3.12
py -3.12 --version  # Verify installation

# Recreate virtual environment
Remove-Item -Recurse -Force venv
py -3.12 -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### Supabase Connection Failed

**Problem**: `Supabase not connected`

**Solution**: Check your `.env` file has the correct credentials:

```powershell
# Test connection
python test_supabase.py
```

### No Products in Database

**Problem**: API returns empty recommendations

**Solution**: Seed the database:

```powershell
python database/seed.py
```

## 📊 Performance Metrics

- **Face Detection**: ~100-200ms (MediaPipe)
- **Skin Analysis**: ~50-100ms (K-Means clustering)
- **Shade Matching**: ~10-20ms (Delta E calculation)
- **Database Query**: ~20-50ms (Supabase)
- **Total Processing**: ~200-400ms per image

Tested on: Windows 11, Intel i7, 16GB RAM

## 🤝 Contributing

This is the backend service for the TrueShade mobile app. 

**Project Status**: Active Development

Feel free to:
- Report bugs via Issues
- Suggest new features
- Submit pull requests
- Add more makeup brands to the database

## 📝 License

MIT License

## 👨‍💻 Author

Built for TrueShade - AI-Powered Makeup Shade Matching

**Contact**: [Your GitHub/Email]

---

**Tech Stack**: Python 3.12 | FastAPI | MediaPipe | OpenCV | scikit-learn | Supabase  
**Color Science**: LAB Color Space | Delta E Distance | K-Means Clustering  
**Computer Vision**: MediaPipe Face Mesh (478 landmarks) | Skin Region Extraction  
**Database**: Supabase PostgreSQL | 89 Products | Real-time Sync

---

⭐ **Star this repo** if you find it useful!

