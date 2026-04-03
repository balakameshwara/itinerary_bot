document.getElementById('itinerary-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // UI Elements
    const btn = document.getElementById('submit-btn');
    const loader = document.getElementById('btn-loader');
    const btnText = btn.querySelector('span');
    const errorMsg = document.getElementById('error-message');
    const resultsSection = document.getElementById('results-section');
    
    // Inputs
    const destination = document.getElementById('destination').value;
    const budget = parseFloat(document.getElementById('budget').value);
    const days = parseInt(document.getElementById('days').value);
    
    // Reset state
    errorMsg.style.display = 'none';
    resultsSection.style.display = 'none';
    btn.disabled = true;
    btnText.textContent = 'Generating...';
    loader.style.display = 'block';
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ destination, budget, days })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to generate itinerary.');
        }
        
        // Update stats
        document.getElementById('stat-places').textContent = data.statistics.visitable_places;
        document.getElementById('stat-cost').textContent = `$${data.statistics.estimated_total_cost.toLocaleString()}`;
        document.getElementById('stat-surplus').textContent = `$${data.statistics.budget_surplus.toLocaleString()}`;
        
        // Render Itinerary
        const board = document.getElementById('itinerary-board');
        board.innerHTML = '';
        
        data.itinerary.forEach(dayInfo => {
            const dayCard = document.createElement('div');
            dayCard.className = 'day-card';
            
            let html = `<h3>Day ${dayInfo.day}</h3><div class="activity-list">`;
            
            dayInfo.activities.forEach(act => {
                html += `
                <div class="activity-item">
                    <div class="activity-main">
                        <h4>${act.place_name}</h4>
                        <p>${act.description}</p>
                    </div>
                    <div class="activity-meta">
                        <span class="cost-badge">$${act.estimated_cost}</span>
                        <a href="${act.map_url}" target="_blank" class="map-btn">📍 Google Maps</a>
                    </div>
                </div>`;
            });
            
            html += `</div>`;
            dayCard.innerHTML = html;
            board.appendChild(dayCard);
        });
        
        resultsSection.style.display = 'flex';
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        errorMsg.textContent = error.message;
        errorMsg.style.display = 'block';
    } finally {
        btn.disabled = false;
        btnText.textContent = 'Generate Itinerary';
        loader.style.display = 'none';
    }
});
