% include('header.tpl')
    <main class="container">
        <div class="row">
          <div class="col-12 text-center">
            <h1> Tags </h1>
          </div>
          <div class="col-12">
                % include('pager.tpl')
                <div class="row">
                  <!-- Portfolio Item 1 -->
                  % for tag in tags:
                  % site_name = tag.site.name if hasattr(tag.site, 'name') else tag.site
                  <div class="col-md-2 col-lg-2 mb-2">
                    <h4> 
                      <a href="/posts?tag={{ tag.clean_name }}&only_questions=True&title=">{{ tag.name }}</a>
                    </h4>
                    <p>
                      Site: <a href="/posts?network_name={{ site_name }}&tag={{ tag.clean_name }}&only_questions=True&title=">{{ site_name }}</a>
                    </p>
                    <p>
                      <span class="badge rounded-pill bg-primary">Questions: {{ tag.questions }}</span>
                    </p>
                  </div>
                  % end
                </div>
            </div>
        </div>
    </main>
% include('footer.tpl')