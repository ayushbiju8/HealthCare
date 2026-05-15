# HealthCare Plus - React Vite Frontend

A modern, responsive healthcare management frontend built with React and Vite.

## 🚀 Features

The frontend provides a complete UI for healthcare management with sample data for all backend models:

### 📊 Dashboard
- Overview of key health metrics
- Quick statistics cards (Health Metrics, Fitness, Medical Reports, Reminders)
- Recent health metrics display
- Quick action buttons for easy navigation

### 👤 Pages Implemented

1. **Dashboard** (`/`)
   - Stats overview with 4 main cards
   - Recent health metrics
   - Quick action menu

2. **User Profile** (`/profile`)
   - User information display
   - Account activity tracking
   - Profile edit button

3. **Health Profile** (`/health-profile`)
   - Personal health information
   - Height, weight, BMI calculation
   - Allergies list
   - Chronic conditions tracker
   - Blood group display

4. **Emergency Contacts** (`/emergency-contacts`)
   - List of emergency contacts
   - Add new contact form
   - Delete contact functionality
   - Contact details (name, relation, phone)

5. **Fitness Summary** (`/fitness`)
   - Daily fitness metrics (steps, heart rate, calories, sleep, SpO2)
   - Multiple day summaries in card layout
   - Weekly statistics table
   - Metric cards with gradient backgrounds

6. **Wearable Integration** (`/wearables`)
   - Connected device management
   - Integration status (active/inactive)
   - Sync functionality
   - Device list with last sync time

7. **Health Metrics** (`/metrics`)
   - Track vital measurements
   - Blood Glucose, Cholesterol, Blood Pressure, Heart Rate
   - Normal range indicators
   - Status badges
   - Add metric form
   - Table view of all metrics

8. **Medical Reports** (`/reports`)
   - Upload and view medical reports
   - Processing status tracking (Pending, Processed, Failed)
   - AI summary display
   - Report type badges
   - Download and view functionality
   - Report statistics

9. **Reminders** (`/reminders`)
   - Health reminders management
   - Medication, vaccination, and checkup reminders
   - Add/edit reminders with recurrence
   - Active/inactive toggle
   - Upcoming reminders preview
   - Reminder statistics

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx          # Navigation component
│   │   └── Navbar.css          # Navigation styles
│   ├── pages/
│   │   ├── Dashboard.jsx       # Main dashboard
│   │   ├── Dashboard.css       # Dashboard styles
│   │   ├── UserProfile.jsx     # User profile page
│   │   ├── HealthProfile.jsx   # Health profile page
│   │   ├── EmergencyContact.jsx# Emergency contacts
│   │   ├── FitnessSummary.jsx  # Fitness tracking
│   │   ├── WearableIntegration.jsx  # Wearable devices
│   │   ├── HealthMetrics.jsx   # Health metrics
│   │   ├── MedicalReports.jsx  # Medical reports
│   │   └── Reminders.jsx       # Health reminders
│   ├── App.jsx                 # Main app component
│   ├── App.css                 # App styles
│   ├── index.css               # Global styles
│   ├── main.jsx                # Entry point
├── public/
├── index.html                  # HTML entry point
├── package.json
├── vite.config.js
└── README.md
```

## 🎨 Styling

- **Global CSS**: Uses CSS custom properties (variables) for consistent theming
- **Color Scheme**:
  - Primary: `#3b82f6` (Blue)
  - Success: `#10b981` (Green)
  - Warning: `#f59e0b` (Amber)
  - Danger: `#ef4444` (Red)
  - Gray scales for neutral elements

- **UI Components**:
  - Cards with shadow effects
  - Metric cards with gradient backgrounds
  - Responsive grid layouts
  - Interactive buttons with hover states
  - Badges for status indicators
  - Alerts for notifications

## 🔧 Available Scripts

### Development Server
```bash
npm run dev
```
Starts the Vite development server at `http://localhost:5173`

### Build
```bash
npm run build
```
Creates optimized production build

### Preview
```bash
npm run preview
```
Preview the production build locally

### Lint
```bash
npm run lint
```
Run ESLint to check code quality

## 📦 Dependencies

- **React**: 18.x - UI library
- **React Router DOM**: 6.x - Client-side routing
- **Lucide React**: Icon library with 1000+ icons
- **Axios**: HTTP client (ready for API integration)
- **Vite**: Build tool and dev server

## 🎯 Backend Integration Ready

The frontend is fully prepared to connect to the Django backend:

1. **API Client Setup**: Axios is already installed
2. **Routes**: All routes map to backend models
3. **Component Structure**: Components are organized by backend models
4. **State Management**: Ready for context API or state management libraries
5. **Sample Data**: All pages include realistic sample data

### To Connect Backend:

1. Create an API service file (`src/services/api.js`):
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const userAPI = {
  getProfile: () => axios.get(`${API_BASE_URL}/users/profile/`),
  updateProfile: (data) => axios.put(`${API_BASE_URL}/users/profile/`, data),
};

// Add more API endpoints as needed
```

2. Update components to fetch real data:
```javascript
useEffect(() => {
  userAPI.getProfile().then(res => setUser(res.data));
}, []);
```

## 📱 Responsive Design

- **Desktop**: Full 2-column layouts where applicable
- **Tablet**: Responsive grid adjustments
- **Mobile**: Single column layouts with collapsible navbar

## 🎨 Customization

To customize the theme, edit the CSS variables in `src/index.css`:

```css
:root {
  --primary: #3b82f6;
  --primary-light: #60a5fa;
  --primary-dark: #1d4ed8;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  /* More colors... */
}
```

## 🚀 Next Steps

1. **Connect Backend API**: Update API endpoints in components
2. **Add Authentication**: Implement login/logout flow
3. **State Management**: Add context API or Redux
4. **Form Validation**: Add form validation libraries
5. **Data Persistence**: Connect to actual API endpoints
6. **Error Handling**: Implement error boundaries and error handling
7. **Loading States**: Add loading spinners
8. **User Notifications**: Add toast notifications

## 📄 License

MIT License - Feel free to use this template for your healthcare projects.

---

**Built with ❤️ using React and Vite**
