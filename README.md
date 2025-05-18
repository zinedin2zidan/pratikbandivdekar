<!DOCTYPE html>
<html>
<head>
    <title>Send Location via WhatsApp</title>
</head>
<body>
    <script>
        function sendLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        const mapsLink = `https://www.google.com/maps?q=${lat},${lng}`;
                        const whatsappNumber = "1234567890"; // Replace with your number (international format)
                        const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(mapsLink)}`;
                        window.location.href = whatsappUrl;
                    },
                    function(error) {
                        alert("Error getting location. Please enable location services.");
                    }
                );
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
        
        // Automatically trigger on page load
        window.onload = sendLocation;
    </script>
</body>
</html>
