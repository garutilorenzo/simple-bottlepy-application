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
                      % if post.score >= 0:
                      % badge_css = 'bg-success'
                      % else:
                      % badge_css = 'bg-danger'
                      % end
                      <span class="badge rounded-pill {{ badge_css }}">{{ post.score }}</span> {{ post.title }} 
                    </p>
                      <p class="custom-font-size-small">
                        % if post.owner:
                        % user_name = post.owner.name
                        <a href="/user/{{ post.owner.id }}/{{  post.owner.clean_name }}" title="{{ post.owner.clean_name }} detail page">{{  post.owner.name }}</a>
                        <span class="badge rounded-pill bg-primary">{{ post.owner.reputation }}</span>
                        % end
                        % if post.accepted_answer_id:
                        <span class="badge rounded-pill bg-info">Answered</span>
                        % end
                      </p>
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