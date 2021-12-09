% include('header.tpl')
    <main class="container">
        <h1>{{ user.name }}</h1>
        <div class="row justify-content-md-center">
            <div class="col-12">
                <p>
                    <span class="badge rounded-pill bg-primary">Views {{ user.views }}</span>
                    <span class="badge rounded-pill bg-success">UP Votes {{ user.up_votes }}</span>
                    <span class="badge rounded-pill bg-danger">DOWN Votes {{ user.down_votes}}</span>
                </p>
                % if user.website:
                <p>
                    <a href="{{ user.website }}">{{ user.name }}</a>
                </p>
                % end
                % if user.about_me:
                <button type="button" class="btn btn-sm btn-outline-info" data-bs-toggle="modal" data-bs-target="#aboutMe">
                    About Me
                </button>

                <div class="modal fade" id="aboutMe" tabindex="-1" aria-labelledby="aboutMeLabel" aria-hidden="true">
                    <div class="modal-dialog">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title" id="aboutMeLabel">About Me</h5>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            {{! user.about_me }}
                        </div>
                        <div class="modal-footer">
                          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                      </div>
                    </div>
                </div>
                % end
            </div>
        </div>
        
        <!-- Icon Divider-->
        <div class="divider-custom divider-light">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>

        <hr class="mt-2 mb-5">
        <h2>Posts</h2>
        <div class="row justify-content-md-center">
            <div class="col-12">
            % if user.posts:
                <table class="table">
                    <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Title</th>
                        <th scope="col">Score</th>
                        <th scope="col">Created</th>
                        <th scope="col">Last activity</th>
                    </tr>
                    </thead>
                    <tbody>
                    % count = 0
                    % for post in user.posts:
                    % count +=1
                    <tr>
                        <th scope="row">{{ count }}</th>
                        % if post.title:
                        <td>
                            <span class="badge rounded-pill bg-primary">Question </span> 
                            <a href="/post/{{ post.id }}/{{ post.clean_title }}" title="{{ post.title }}">{{ post.title }}</a>
                        </td>
                        % else:
                        <td>
                            <span class="badge rounded-pill bg-info">Answer </span> 
                            <a href="/post/{{ post.question.id }}/{{ post.question.clean_title }}" title="{{ post.question.title }}">{{ post.question.title }}</a>
                        </td>
                        % end
                        <td>{{ post.score }}</td>
                        <td>{{ post.created_time.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                        <td>{{ post.last_activity_date.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                    %end
                    </tbody>
                </table>
            % end
            </div>
        </div>
    </main>
% include('footer.tpl')