% include('header.tpl')
    <main class="container">
        <div class="row justify-content-md-center">
            <div class="col-8">
                <h1>{{ post.title }}</h1>
                <p>
                    <span class="badge rounded-pill bg-primary">Views {{ post.view_count }}</span>
                    <span class="badge rounded-pill bg-success">Score {{ post.score }}</span>
                </p>
            </div>
        </div>    
        <div class="row justify-content-md-center">
            <div class="col-8">
                
                % if post.post_history:
                <button type="button" class="btn btn-sm btn-outline-info" data-bs-toggle="modal" data-bs-target="#postHistory">
                    Post History
                </button>

                <div class="modal fade" id="postHistory" tabindex="-1" aria-labelledby="postHistoryLabel" aria-hidden="true">
                    <div class="modal-dialog  modal-lg">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title" id="postHistoryLabel">Post History</h5>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <table class="table">
                                <thead>
                                  <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Detail</th>
                                    <th scope="col">Event Type</th>
                                    <th scope="col">RevisionGuid</th>
                                    <th scope="col">Date</th>
                                  </tr>
                                </thead>
                                <tbody>
                                    % count = 0
                                    % for event in post.post_history:
                                    % count +=1
                                    <tr>
                                        <th scope="row">{{ count }}</th>
                                        % if event.text:
                                        <td>{{ event.text }}</td>
                                        % elif event.comment:
                                        <td>{{ event.comment }}</td>
                                        % end
                                        <td>{{ event.post_history_type.name }}</td>
                                        <td>{{ event.revision_guid }}</td>
                                        <td>{{ event.created_time.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                                    </tr>
                                    % end
                                </tbody>
                            </table>                            
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
        <div class="row justify-content-md-center">
            <div class="col-8">
                {{! post.body }}
            </div>
        </div>
        <!-- Icon Divider-->
        <div class="divider-custom divider-light">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>

        <hr class="mt-2 mb-5">
        <div class="row justify-content-md-center">
            <div class="col-8">
                <h2>Answers</h2>
            </div>
        </div>
        % if post.answers:
        % for answer in post.answers:
        <div class="row justify-content-md-center mb-4">
            <div class="col-8  border border-1">                
                {{! answer.body }}
            </div>
        </div>
        % end
        % end
    </main>
% include('footer.tpl')