% include('header.tpl')
    <main class="container">
        <div class="row">
            <div class="col-12">
              % include('pager.tpl')
              <div class="row">
                <!-- Portfolio Item 1 -->
                % for post in posts:
                <div class="col-md-4 col-lg-4 mb-4">
                    <h4> 
                        <a href="/post/{{ post.id }}/{{ post.clean_title }}" title="{{ post.title }}">{{ post.id }} {{ post.title }}</a>
                    </h4>
                      % if post.owner_user:
                      % user_name = post.owner_user.name
                      <p>
                        <a href="/user/{{ post.owner_user.id }}/{{  post.owner_user.clean_name }}" title="{{ post.owner_user.clean_name }} detail page">{{  post.owner_user.name }}</a>
                        <span class="badge rounded-pill bg-primary">User reputation {{ post.owner_user.reputation }}</span>
                      </p>
                      % end
                </div>
                % end
              </div>
            </div>
        </div>
    </main>
% include('footer.tpl')