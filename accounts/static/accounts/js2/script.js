var deleteFaq = document.getElementsByClassName('text-red');
var faqEntry = document.getElementsByClassName('faq-content');

deleteFaq.addEventListener('click', remove());

function remove() {
    faqEntry.remove();
}