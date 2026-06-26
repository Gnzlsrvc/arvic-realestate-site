document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('js-reveal-ready');

  initFeaturedGrids();
  initOfficeListings();
  initRevealAnimations();
});

const PLACEHOLDER_CLASSES = ['placeholder-1', 'placeholder-2', 'placeholder-3'];

function shortTag(status) {
  if (!status) return 'View';
  if (/^Sold/i.test(status)) return 'Sold';
  if (/auction/i.test(status)) return 'Auction';
  if (/negotiation/i.test(status)) return 'By Negotiation';
  if (/tender/i.test(status)) return 'Tender';
  if (/deadline/i.test(status)) return 'Deadline Sale';
  if (/asking price/i.test(status)) return 'Asking Price';
  if (/set date of sale/i.test(status)) return 'Set Sale Date';
  if (/enquir/i.test(status)) return 'Enquire';
  if (/off market/i.test(status)) return 'Off Market';
  return status.length > 18 ? status.slice(0, 18) + '…' : status;
}

function cardHTML(listing, i) {
  const imgClass = PLACEHOLDER_CLASSES[i % PLACEHOLDER_CLASSES.length];
  const metaParts = [];
  if (listing.beds) metaParts.push(`${listing.beds} bed`);
  if (listing.baths) metaParts.push(`${listing.baths} bath`);
  if (listing.cars) metaParts.push(`${listing.cars} car`);
  const meta = metaParts.length ? `<ul class="meta"><li>${metaParts.join('</li><li>')}</li></ul>` : '';
  return `
    <article class="listing-card">
      <a class="listing-img ${imgClass}" href="${listing.href}" target="_blank" rel="noopener"><span class="tag">${shortTag(listing.status)}</span></a>
      <div class="listing-body">
        <h3 class="card-address">${listing.address}</h3>
        <p class="card-suburb">${listing.suburb} · ${listing.status}</p>
        ${meta}
        <a href="${listing.href}" target="_blank" rel="noopener" class="view-link">View Listing →</a>
      </div>
    </article>`;
}

function initFeaturedGrids() {
  if (typeof OFFICE_LISTINGS === 'undefined') return;

  const featuredGrid = document.getElementById('featured-listing-grid');
  const soldGrid = document.getElementById('featured-sold-grid');
  const showMoreBtn = document.getElementById('sold-show-more');

  if (featuredGrid) {
    const forSale = OFFICE_LISTINGS.filter(l => l.type === 'for-sale').slice(0, 3);
    featuredGrid.innerHTML = forSale.map(cardHTML).join('');
  }

  if (soldGrid) {
    const allSold = OFFICE_LISTINGS.filter(l => l.type === 'sold');
    const pageSize = 6;
    let shown = pageSize;

    function renderSold() {
      soldGrid.innerHTML = allSold.slice(0, shown).map(cardHTML).join('');
      if (showMoreBtn) {
        showMoreBtn.style.display = shown >= allSold.length ? 'none' : 'inline-block';
      }
    }

    renderSold();

    if (showMoreBtn) {
      showMoreBtn.addEventListener('click', () => {
        shown += pageSize;
        renderSold();
      });
    }
  }
}

function initOfficeListings() {
  const grid = document.getElementById('office-listing-grid');
  const select = document.getElementById('office-suburb-select');
  const countEl = document.getElementById('office-results-count');
  const statusButtons = document.querySelectorAll('.status-pills .filter-btn');
  const prevBtn = document.getElementById('office-prev-page');
  const nextBtn = document.getElementById('office-next-page');
  const pageIndicator = document.getElementById('office-page-indicator');
  if (!grid || typeof OFFICE_LISTINGS === 'undefined') return;

  const PAGE_SIZE = 9;
  let currentPage = 1;

  const suburbs = Array.from(new Set(OFFICE_LISTINGS.map(l => l.suburb))).sort();
  suburbs.forEach(suburb => {
    const opt = document.createElement('option');
    opt.value = suburb;
    opt.textContent = suburb;
    select.appendChild(opt);
  });

  function getFiltered() {
    const suburb = select.value;
    const status = document.querySelector('.status-pills .filter-btn.active').dataset.status;
    return OFFICE_LISTINGS.filter(l => {
      const suburbMatch = suburb === 'all' || l.suburb === suburb;
      const statusMatch = status === 'all' || l.type === status;
      return suburbMatch && statusMatch;
    });
  }

  function render() {
    const filtered = getFiltered();
    const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    currentPage = Math.min(currentPage, totalPages);

    const start = (currentPage - 1) * PAGE_SIZE;
    const pageItems = filtered.slice(start, start + PAGE_SIZE);

    grid.innerHTML = pageItems.map(cardHTML).join('');
    countEl.textContent = `Showing ${filtered.length} ${filtered.length === 1 ? 'property' : 'properties'} (sold results limited to the last 6 months)`;
    pageIndicator.textContent = `Page ${currentPage} of ${totalPages}`;
    prevBtn.disabled = currentPage <= 1;
    nextBtn.disabled = currentPage >= totalPages;
  }

  select.addEventListener('change', () => { currentPage = 1; render(); });
  statusButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      statusButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentPage = 1;
      render();
    });
  });
  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) { currentPage--; render(); scrollToGrid(); }
  });
  nextBtn.addEventListener('click', () => {
    currentPage++; render(); scrollToGrid();
  });

  function scrollToGrid() {
    grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  render();
}

function initRevealAnimations() {
  const revealEls = document.querySelectorAll('.reveal');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0, rootMargin: '0px 0px -100px 0px' });

  revealEls.forEach(el => observer.observe(el));
}
