/**
 * Prediction Page JavaScript
 * Enhanced with modern UI interactions
 */

const API_BASE_URL = window.location.origin;

// Map variables (works with both OpenStreetMap and Google Maps)
let map;
let marker;
let geocoder;
let autocomplete;
let useGoogleMaps = false;

// Initialize Map (OpenStreetMap by default, Google Maps if available)
function initMap() {
    // Check if Google Maps is available
    const hasGoogleMapsKey = window.google_maps_key && window.google_maps_key !== 'YOUR_API_KEY';
    if (typeof google !== 'undefined' && google.maps && hasGoogleMapsKey) {
        useGoogleMaps = true;
        initGoogleMap();
    } else {
        // Use OpenStreetMap (free, no API key needed)
        initOpenStreetMap();
    }
}

// Initialize OpenStreetMap with Leaflet (FREE, no API key)
function initOpenStreetMap() {
    // Default center (India)
    const defaultCenter = [20.5937, 78.9629];
    
    // Initialize Leaflet map
    map = L.map('map', {
        center: defaultCenter,
        zoom: 5,
        zoomControl: true,
        attributionControl: true
    });
    
    // Add dark theme tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Add dark theme alternative (CartoDB Dark Matter)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors, © CARTO',
        subdomains: 'abcd',
        maxZoom: 19
    }).addTo(map);
    
    // Create marker
    marker = L.marker(defaultCenter, {
        draggable: true,
        icon: L.divIcon({
            className: 'custom-marker',
            html: '<div style="background: linear-gradient(135deg, #00f5ff, #7b2ff7); width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 20px rgba(0, 245, 255, 0.8);"></div>',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        })
    }).addTo(map);
    
    // Add click listener to map
    map.on('click', (e) => {
        placeMarkerAndGetCoordinates([e.latlng.lat, e.latlng.lng]);
    });
    
    // Add drag listener to marker
    marker.on('dragend', (e) => {
        const position = marker.getLatLng();
        updateCoordinates([position.lat, position.lng]);
    });
    
    // Initialize address search with Nominatim (free geocoding)
    setupNominatimSearch();
}

// Initialize Google Maps (if API key is available)
function initGoogleMap() {
    // Default center (India - approximate center)
    const defaultCenter = { lat: 20.5937, lng: 78.9629 };
    
    // Initialize map
    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultCenter,
        zoom: 5,
        styles: [
            {
                featureType: 'all',
                elementType: 'geometry',
                stylers: [{ color: '#1a1a2e' }]
            },
            {
                featureType: 'all',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#00f5ff' }]
            },
            {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{ color: '#0a0e27' }]
            },
            {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{ color: '#1a1a2e' }]
            }
        ],
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: true
    });
    
    // Initialize geocoder
    geocoder = new google.maps.Geocoder();
    
    // Initialize marker
    marker = new google.maps.Marker({
        map: map,
        draggable: true,
        animation: google.maps.Animation.DROP,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 10,
            fillColor: '#00f5ff',
            fillOpacity: 1,
            strokeColor: '#7b2ff7',
            strokeWeight: 3
        }
    });
    
    // Add click listener to map
    map.addListener('click', (e) => {
        placeMarkerAndGetCoordinates(e.latLng);
    });
    
    // Add drag listener to marker
    marker.addListener('dragend', (e) => {
        updateCoordinates(e.latLng);
    });
    
    // Initialize address autocomplete
    const addressInput = document.getElementById('address');
    if (addressInput) {
        autocomplete = new google.maps.places.Autocomplete(addressInput, {
            types: ['geocode', 'establishment'],
            componentRestrictions: { country: 'in' }
        });
        
        autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place.geometry) {
                const location = place.geometry.location;
                placeMarkerAndGetCoordinates(location);
                map.setCenter(location);
                map.setZoom(15);
            }
        });
    }
}

// Setup Nominatim search for OpenStreetMap (free geocoding)
function setupNominatimSearch() {
    const addressInput = document.getElementById('address');
    if (!addressInput) return;
    
    let searchTimeout;
    addressInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value;
        
        if (query.length < 3) return;
        
        searchTimeout = setTimeout(() => {
            searchAddress(query);
        }, 500);
    });
}

// Search address using Nominatim (free)
async function searchAddress(query) {
    try {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=in`
        );
        const data = await response.json();
        
        if (data && data.length > 0) {
            const result = data[0];
            const lat = parseFloat(result.lat);
            const lon = parseFloat(result.lon);
            placeMarkerAndGetCoordinates([lat, lon]);
        }
    } catch (error) {
        console.error('Geocoding error:', error);
    }
}

// Universal function to place marker (works with both map types)
function placeMarkerAndGetCoordinates(location) {
    if (useGoogleMaps) {
        // Google Maps
        marker.setPosition(location);
        map.setCenter(location);
        map.setZoom(15);
        updateCoordinates(location);
    } else {
        // OpenStreetMap
        const [lat, lng] = Array.isArray(location) ? location : [location.lat, location.lng];
        marker.setLatLng([lat, lng]);
        map.setView([lat, lng], 15);
        updateCoordinates([lat, lng]);
    }
}

// Universal function to update coordinates (works with both map types)
function updateCoordinates(location) {
    let lat, lng;
    
    if (useGoogleMaps) {
        lat = location.lat();
        lng = location.lng();
    } else {
        [lat, lng] = Array.isArray(location) ? location : [location.lat, location.lng];
    }
    
    document.getElementById('latitude').value = lat.toFixed(6);
    document.getElementById('longitude').value = lng.toFixed(6);
    
    // Reverse geocode to get address
    if (useGoogleMaps) {
        geocoder.geocode({ location: location }, (results, status) => {
            if (status === 'OK' && results[0]) {
                document.getElementById('address').value = results[0].formatted_address;
            }
        });
    } else {
        // Use Nominatim for reverse geocoding (free)
        reverseGeocodeNominatim(lat, lng);
    }
}

// Reverse geocode using Nominatim (free)
async function reverseGeocodeNominatim(lat, lng) {
    try {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
        );
        const data = await response.json();
        
        if (data && data.display_name) {
            document.getElementById('address').value = data.display_name;
        }
    } catch (error) {
        console.error('Reverse geocoding error:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    
    // Add smooth page transition
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in';
        document.body.style.opacity = '1';
    }, 100);
    
    // Check API health
    checkHealth();
    
    // Setup form validation
    setupFormValidation();
    
    // Setup input animations
    setupInputAnimations();
    
    // Initialize map (OpenStreetMap by default, Google Maps if available)
    // Check if we're waiting for Google Maps callback
    if (typeof google !== 'undefined' && google.maps) {
        initMap();
    } else {
        // Try to initialize OpenStreetMap immediately
        // If Google Maps callback is set, it will override
        window.initMap = initMap;
        
        // Initialize OpenStreetMap if Google Maps doesn't load
        setTimeout(() => {
            if (!map) {
                initMap(); // Will use OpenStreetMap
            }
        }, 1000);
    }
    
    // Setup form submission handler
    const form = document.getElementById('predictionForm');
    if (form) {
        
        // Attach form submission handler
        form.addEventListener('submit', handleFormSubmit);
    } else {
        console.error('Prediction form not found!');
    }
});

// Form submission handler function
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    let data = {};
    
    // Initialize all required fields with defaults (especially checkboxes)
    data['UNDER_CONSTRUCTION'] = 0;
    data['RERA'] = 0;
    data['READY_TO_MOVE'] = 0;
    data['RESALE'] = 0;
    
    // Convert form data to object
    for (const [key, value] of formData.entries()) {
        // Handle checkboxes - if checkbox is checked, it will be in formData
        if (key === 'UNDER_CONSTRUCTION' || key === 'RERA' || key === 'READY_TO_MOVE' || key === 'RESALE') {
            data[key] = value === '1' || value === 'on' ? 1 : 0;
        }
        // Convert numeric fields
        else if (['BHK_NO.', 'SQUARE_FT', 'LONGITUDE', 'LATITUDE'].includes(key)) {
            const numValue = parseFloat(value);
            data[key] = isNaN(numValue) ? 0 : numValue;
        } else {
            data[key] = value || '';
        }
    }
    
    // Ensure numeric fields are numbers, not strings
    if (data['BHK_NO.']) data['BHK_NO.'] = parseFloat(data['BHK_NO.']) || 0;
    if (data['SQUARE_FT']) data['SQUARE_FT'] = parseFloat(data['SQUARE_FT']) || 0;
    if (data['LONGITUDE']) data['LONGITUDE'] = parseFloat(data['LONGITUDE']) || 0;
    if (data['LATITUDE']) data['LATITUDE'] = parseFloat(data['LATITUDE']) || 0;
    
    // CRITICAL: Ensure all required checkbox fields are present (even if 0)
    // Unchecked checkboxes don't appear in FormData, so we must explicitly include them
    if (!('UNDER_CONSTRUCTION' in data)) data['UNDER_CONSTRUCTION'] = 0;
    if (!('RERA' in data)) data['RERA'] = 0;
    if (!('READY_TO_MOVE' in data)) data['READY_TO_MOVE'] = 0;
    if (!('RESALE' in data)) data['RESALE'] = 0;
    
    // Validate required fields
    if (!data['BHK_OR_RK'] || !data['BHK_NO.'] || !data['SQUARE_FT'] || !data['POSTED_BY'] || !data['LONGITUDE'] || !data['LATITUDE']) {
        showError('Please fill in all required fields (marked with *)');
        return;
    }
    
    // Add missing required fields for the model
    if (!data['area']) data['area'] = data['SQUARE_FT'];
    if (!data['bedrooms']) data['bedrooms'] = data['BHK_NO.'];
    if (!data['longitude']) data['longitude'] = data['LONGITUDE'];
    if (!data['latitude']) data['latitude'] = data['LATITUDE'];
    if (!data['CITY_NAME']) data['CITY_NAME'] = data['ADDRESS'] || 'Unknown';
    
    // CRITICAL: Ensure all required checkbox fields are present with numeric values
    // These must be included even if checkboxes are unchecked
    data['UNDER_CONSTRUCTION'] = data['UNDER_CONSTRUCTION'] !== undefined ? parseInt(data['UNDER_CONSTRUCTION']) || 0 : 0;
    data['RERA'] = data['RERA'] !== undefined ? parseInt(data['RERA']) || 0 : 0;
    data['READY_TO_MOVE'] = data['READY_TO_MOVE'] !== undefined ? parseInt(data['READY_TO_MOVE']) || 0 : 0;
    data['RESALE'] = data['RESALE'] !== undefined ? parseInt(data['RESALE']) || 0 : 0;
    
    // Reorder data to match expected feature order from preprocessor
    // Expected order from preprocessor.feature_names:
    const expectedOrder = ['POSTED_BY', 'UNDER_CONSTRUCTION', 'RERA', 'BHK_NO.', 'BHK_OR_RK', 'SQUARE_FT', 'READY_TO_MOVE', 'RESALE', 'ADDRESS', 'LONGITUDE', 'LATITUDE', 'area', 'bedrooms', 'longitude', 'latitude', 'CITY_NAME'];
    const orderedData = {};
    // Add fields in expected order
    for (const key of expectedOrder) {
        if (key in data) {
            orderedData[key] = data[key];
        }
    }
    // Add any extra keys that might exist (shouldn't happen, but just in case)
    for (const key in data) {
        if (!(key in orderedData)) {
            orderedData[key] = data[key];
        }
    }
    data = orderedData;
    
    // Show loading state
    setLoadingState(true);
    hideResults();
    hideError();
    
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            
            // Build detailed error message
            let errorMsg = result.error || 'Prediction failed';
            if (result.received_columns && result.expected_columns) {
                errorMsg += '\n\nReceived columns: ' + result.received_columns.join(', ');
                errorMsg += '\nExpected columns: ' + (Array.isArray(result.expected_columns) ? result.expected_columns.join(', ') : result.expected_columns);
            }
            if (result.details) {
                errorMsg += '\n\nDetails: ' + result.details;
            }
            if (result.hint) {
                errorMsg += '\n\nHint: ' + result.hint;
            }
            
            console.error('API Error:', result);
            showError(errorMsg, result);
            return; // Don't throw, just show error
        }
        
        // Display results with animation
        setTimeout(() => {
            displayResults(result);
        }, 300);
        
    } catch (error) {
        console.error('Prediction error:', error);
        let errorMsg = error.message || 'Failed to get prediction. Please try again.';
        if (error.message && error.message.includes('fetch')) {
            errorMsg = 'Cannot connect to server. Make sure the server is running on http://localhost:5001';
        }
        showError(errorMsg);
    } finally {
        setLoadingState(false);
    }
}

function showMapError() {
    const mapContainer = document.getElementById('map-container');
    if (mapContainer) {
        mapContainer.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; padding: 20px; text-align: center; color: var(--text-secondary);">
                <div style="font-size: 3rem; margin-bottom: 20px;">🗺️</div>
                <h3 style="color: var(--primary-cyan); margin-bottom: 10px;">Google Maps API Key Required</h3>
                <p style="margin-bottom: 15px;">To use the map picker, you need to add your Google Maps API key.</p>
                <div style="background: rgba(0, 0, 0, 0.5); padding: 15px; border-radius: 10px; border: 1px solid var(--glass-border); max-width: 500px;">
                    <p style="margin-bottom: 10px;"><strong>Quick Setup:</strong></p>
                    <ol style="text-align: left; margin-left: 20px;">
                        <li>Get free API key from <a href="https://console.cloud.google.com/" target="_blank" style="color: var(--primary-cyan);">Google Cloud Console</a></li>
                        <li>Enable: Maps JavaScript API, Places API, Geocoding API</li>
                        <li>Set environment variable: <code style="background: rgba(0,245,255,0.1); padding: 2px 6px; border-radius: 4px;">export GOOGLE_MAPS_API_KEY="your_key"</code></li>
                        <li>Or edit predict.html and replace YOUR_API_KEY</li>
                    </ol>
                    <p style="margin-top: 15px; font-size: 0.9rem;">See <code style="background: rgba(0,245,255,0.1); padding: 2px 6px; border-radius: 4px;">GET_API_KEY.md</code> for detailed instructions</p>
                </div>
                <p style="margin-top: 20px; font-size: 0.9rem;">You can still enter coordinates manually below ⬇️</p>
            </div>
        `;
    }
}

function setLoadingState(loading) {
    const btn = document.getElementById('predictBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const btnContent = btn.querySelector('.btn-content');
    
    if (loading) {
        btn.disabled = true;
        btnText.textContent = 'Predicting...';
        btnLoader.style.display = 'block';
        btnContent.style.opacity = '0.5';
    } else {
        btn.disabled = false;
        btnText.textContent = 'Predict Price';
        btnLoader.style.display = 'none';
        btnContent.style.opacity = '1';
    }
}

function displayResults(result) {
    const resultsCard = document.getElementById('resultsCard');
    const priceElement = document.getElementById('predictedPrice');
    const timeElement = document.getElementById('inferenceTime');
    
    // Format price in Indian currency
    const price = result.predicted_price || result.predictions?.[0];
    priceElement.textContent = formatCurrency(price);
    
    // Animate price number
    animateValue(priceElement, 0, price, 1000, formatCurrency);
    
    // Display inference time
    const time = result.inference_time_ms || result.model_inference_time_ms || 0;
    timeElement.textContent = `${time.toFixed(2)} ms`;
    
    // Show results card with animation
    resultsCard.style.display = 'block';
    resultsCard.style.opacity = '0';
    resultsCard.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        resultsCard.style.transition = 'all 0.5s ease-out';
        resultsCard.style.opacity = '1';
        resultsCard.style.transform = 'translateY(0)';
    }, 50);
    
    // Scroll to results
    setTimeout(() => {
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 600);
}

function animateValue(element, start, end, duration, formatter) {
    const startTime = performance.now();
    const range = end - start;
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = start + (range * easeOutQuart);
        
        element.textContent = formatter(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = formatter(end);
        }
    }
    
    requestAnimationFrame(update);
}

function formatCurrency(amount) {
    if (!amount || amount === 0) return '₹0';
    
    // Format in Indian numbering system (Lakhs/Crores)
    const crores = amount / 10000000;
    const lakhs = amount / 100000;
    
    if (crores >= 1) {
        return `₹${crores.toFixed(2)} Cr`;
    } else if (lakhs >= 1) {
        return `₹${lakhs.toFixed(2)} L`;
    } else {
        return `₹${Math.round(amount).toLocaleString('en-IN')}`;
    }
}

function showError(message, details = null) {
    const errorCard = document.getElementById('errorCard');
    const errorMessage = document.getElementById('errorMessage');
    
    let fullMessage = message;
    if (details) {
        if (typeof details === 'string') {
            fullMessage += '\n\n' + details;
        } else if (details.error) {
            fullMessage += '\n\nError: ' + details.error;
            if (details.hint) {
                fullMessage += '\n\nHint: ' + details.hint;
            }
        }
    }
    
    errorMessage.innerHTML = fullMessage.replace(/\n/g, '<br>');
    errorCard.style.display = 'block';
    errorCard.style.opacity = '0';
    errorCard.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        errorCard.style.transition = 'all 0.3s ease-out';
        errorCard.style.opacity = '1';
        errorCard.style.transform = 'scale(1)';
    }, 50);
    
    errorCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideError() {
    const errorCard = document.getElementById('errorCard');
    errorCard.style.transition = 'all 0.3s ease-out';
    errorCard.style.opacity = '0';
    errorCard.style.transform = 'scale(0.9)';
    setTimeout(() => {
        errorCard.style.display = 'none';
    }, 300);
}

function hideResults() {
    const resultsCard = document.getElementById('resultsCard');
    resultsCard.style.transition = 'all 0.3s ease-out';
    resultsCard.style.opacity = '0';
    resultsCard.style.transform = 'translateY(20px)';
    setTimeout(() => {
        resultsCard.style.display = 'none';
    }, 300);
}

function checkHealth() {
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(health => {
            if (!health.model_loaded) {
                console.warn('Model not loaded yet');
            }
        })
        .catch(error => {
            console.error('Health check failed:', error);
        });
}

function setupFormValidation() {
    const inputs = document.querySelectorAll('.form-input, .form-select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value) {
                this.style.borderColor = 'var(--error-red)';
            } else {
                this.style.borderColor = 'var(--glass-border)';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.style.borderColor === 'rgb(239, 68, 68)') {
                this.style.borderColor = 'var(--glass-border)';
            }
        });
    });
}

function setupInputAnimations() {
    const inputs = document.querySelectorAll('.form-input, .form-select');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.2s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });
}

// Format number inputs
document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', function() {
        if (this.value && parseFloat(this.value) < 0) {
            this.value = 0;
        }
    });
});

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

