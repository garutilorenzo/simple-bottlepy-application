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
                  <div class="col-md-2 col-lg-2 mb-2">
                    <h4> 
                      <a href="/posts/{{ tag.clean_name }}">{{ tag.name }}</a>
                    </h4>
                    <p>
                      Site: <a href="/posts/{{ tag.clean_name }}-{{ tag.site.name }}">{{ tag.site.name }}</a>
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