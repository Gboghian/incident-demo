# Basic HTML Incident Report Forms

This directory contains three versions of basic HTML forms for incident submission, each designed for different use cases.

## Form Versions

### 1. Simple Incident Form (`simple_incident_form.html`)
- **Purpose:** Minimal, unstyled HTML form
- **Features:**
  - Basic HTML5 form elements
  - Required field validation
  - Placeholder text for guidance
  - No external dependencies
- **Use Case:** Quick integration, minimal styling needs

### 2. Basic Incident Form (`basic_incident_form.html`)
- **Purpose:** Styled form with embedded CSS
- **Features:**
  - Clean, modern styling with embedded CSS
  - Form validation with JavaScript
  - Character counter for description field
  - Responsive design
  - Visual feedback for validation
- **Use Case:** Standalone form with professional appearance

### 3. Bootstrap Incident Form (`bootstrap_incident_form.html`)
- **Purpose:** Fully styled form using Bootstrap framework
- **Features:**
  - Bootstrap 5 styling and components
  - Font Awesome icons
  - Comprehensive help section
  - Advanced form validation
  - Mobile-responsive design
  - Professional UI/UX
- **Use Case:** Integration with Bootstrap-based applications

## Form Fields

All forms include the following required fields:

1. **Equipment** (Text Input)
   - Equipment involved in the incident
   - Examples: "Conveyor Belt #3", "Hydraulic Press A2"
   - Required field

2. **Location** (Text Input)
   - Physical location where incident occurred
   - Examples: "Production Floor A", "Warehouse Section B"
   - Required field

3. **Description** (Textarea)
   - Detailed description of the incident
   - Minimum 10 characters required
   - Includes guidance for what to include
   - Required field

4. **Submit Button**
   - Submits form data to `/report` endpoint
   - Includes form validation before submission

## Form Submission

All forms are configured to submit to the `/report` endpoint using POST method:
```html
<form action="/report" method="POST">
```

## Validation Features

- **Client-side validation:** HTML5 required attributes and JavaScript validation
- **Field validation:** Checks for empty fields and minimum description length
- **User feedback:** Visual indicators and alert messages for validation errors
- **Character counting:** Real-time character count for description field (styled versions)

## Integration Notes

- Forms are designed to work with the Flask `/report` route
- Field names match the IncidentForm Flask-WTF form fields
- Bootstrap version matches the application's existing styling
- All forms include proper form action and method attributes

## Browser Compatibility

- All forms use standard HTML5 and are compatible with modern browsers
- JavaScript validation enhances user experience but is not required for submission
- Bootstrap version requires internet connection for CDN resources

## Customization

Each form can be easily customized:
- Modify field labels and placeholders
- Adjust validation rules
- Change styling and layout
- Add additional fields as needed
- Integrate with different backend endpoints
