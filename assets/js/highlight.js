document.addEventListener("DOMContentLoaded", function() {
    // Function to get the value of a query parameter
    function getQueryParam(name) {
        return new URLSearchParams(window.location.search).get(name);
    }

    // Function to highlight search terms in the content
    function highlightSearchTerm(term) {
        if (!term) return;

        const content = document.querySelector('.post-content'); // Change selector to match your post content
        if (!content) return;

        const regex = new RegExp(`(${term})`, 'gi');
        content.innerHTML = content.innerHTML.replace(regex, '<mark>$1</mark>');
    }

    const searchTerm = getQueryParam('search');
    highlightSearchTerm(searchTerm);
});
