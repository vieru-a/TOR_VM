function business_type_select(value) {
    let divs = document.getElementsByClassName('type-select')
    for (let i = 0; i < divs.length; i++) {
        if (value === 'legal_entities') {
            divs[i].style.display = 'block';
        }
        else {
            divs[i].style.display = "None";
        }
    }
}