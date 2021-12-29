    <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">BottlePy
                <img src="/static/img/bottle_nav.png" alt="" width="30" height="24" class="d-inline-block align-text-top">
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                % for page in nav_pages:
                % nav_page_css = ''
                % if page.name.lower() == page_name:
                % nav_page_css = 'active'
                % end
                <li class="nav-item">
                    <a class="nav-link {{ nav_page_css }}" href="{{ page.url }}">{{ page.name }}</a>
                </li>
                % end
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                      More
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                      % for d_page in nav_dropdown_pages:
                      <li><a class="dropdown-item" href="{{ d_page.url }}">{{ d_page.name }}</a></li>
                      % end
                    </ul>
                  </li>
            </ul>
            <form class="d-flex">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            </div>
        </div>
    </nav>