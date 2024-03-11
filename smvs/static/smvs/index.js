function loadForms() {
    var numCandidates = document.getElementById('id_num_candidates').value;
    var formContainer = document.getElementById('form-container');
    formContainer.innerHTML = ''; // Clear previous forms

    for (var i = 0; i < numCandidates; i++) {
        var form = `
            <form method="post" action="{% url 'createCandidate' %}" enctype="multipart/form-data">
                {% csrf_token %}
                <div>
                    <label for="id_first_name_${i}">First Name:</label>
                    <input type="text" id="id_first_name_${i}" name="first_name">
                </div>
                <div>
                    <label for="id_middle_name">Middle Name:</label>
                    <input type="text" id="id_middle_name" name="middle_name">
                </div>
                <div>
                    <label for="id_last_name">Last Name:</label>
                    <input type="text" id="id_last_name" name="last_name">
                </div>
                <div>
                    <label for="id_email">Email:</label>
                    <input type="email" id="id_email" name="email">
                </div>
                <div>
                    <label for="id_phone_number">Phone Number:</label>
                    <input type="text" id="id_phone_number" name="phone_number">
                </div>
                <div>
                    <label for="id_party_affiliation">Party Affiliation:</label>
                    <input type="text" id="id_party_affiliation" name="party_affiliation">
                </div>
                <div>
                    <label for="id_profile_picture">Profile Picture:</label>
                    <input type="file" id="id_profile_picture" name="profile_picture">
                </div>
                <input type="submit" value="Submit">
            </form>
        `;
        formContainer.innerHTML += form;
    }
}