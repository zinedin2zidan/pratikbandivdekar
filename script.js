
document.getElementById('studentForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = {
    studentName: document.getElementById('studentName').value,
    contactNumber: document.getElementById('contactNumber').value,
    parentContact: document.getElementById('parentContact').value,
    location: document.getElementById('location').value
  };

  try {
    const response = await fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      alert('Data submitted successfully!');
      document.getElementById('studentForm').reset();
    } else {
      alert('Error submitting data');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Error submitting data');
  }
});
