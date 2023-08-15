
// JavaScript code to handle the selection change event
const studentSelect = document.getElementById('studentSelect');
const lastNameInput = document.getElementById('full_name');

studentSelect.addEventListener('change', () => {
    const selectedStudent = studentSelect.options[studentSelect.selectedIndex];
    const studentName = selectedStudent.text.trim();
    const [firstName, lastName] = studentName.split(' ');

    // Set the values of other fields based on the selected student
    full_name.value = lastName;
    console.log(full_name)

    // Add similar code for other fields
});
