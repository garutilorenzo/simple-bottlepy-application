% include('header.tpl')
    <main class="container">
        <div class="row">
            <div class="col-12 text-center">
              <h1> Posts </h1>
            </div>
            <div class="col-12">
              % include('pager.tpl')
              <div class="row">
                <!-- Portfolio Item 1 -->
                % for post in posts:
                <div class="col-md-4 col-lg-4 mb-4">
                    <p> 
                        {{ post.title }}
                    </p>
                      % if post.owner:
                      % user_name = post.owner.name
                      <p class="custom-font-size-small">
                        <a href="/user/{{ post.owner.id }}/{{  post.owner.clean_name }}" title="{{ post.owner.clean_name }} detail page">{{  post.owner.name }}</a>
                        <span class="badge rounded-pill bg-primary">{{ post.owner.reputation }}</span>
                      </p>
                      % end
                      <p>
                        <a href="/post/{{ post.id }}/{{ post.clean_title }}" class="btn btn-primary btn-sm" title="{{ post.title }}">Detail</a>
                      </p>
                </div>
                % end
              </div>
            </div>
        </div>
    </main>
% include('footer.tpl')