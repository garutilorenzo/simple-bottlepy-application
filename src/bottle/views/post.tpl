% include('header.tpl')
    <main class="container">
        <div class="row justify-content-md-center">
            <div class="col-12">
                <h1>{{ post.title }}</h1>
                <p>
                    % if post.score >= 0:
                    % badge_css = 'bg-success'
                    % else:
                    % badge_css = 'bg-danger'
                    % end
                    Views <span class="badge rounded-pill bg-primary">{{ post.view_count }}</span>
                    Score <span class="badge rounded-pill {{ badge_css }}">{{ post.score }}</span>
                </p>
            </div>
        </div>
        <div class="row justify-content-md-center  mb-4">
            <div class="col-12">
                % if post.accepted_answer_id:
                <a href="#answer-id-{{ post.accepted_answer_id }}" class="btn btn-sm btn-outline-info">Go to the answer</a>
                % end
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
                                    % event_type = event.post_history_type.name if hasattr(event.post_history_type, 'name') else event.post_history_type
                                    % count +=1
                                    <tr>
                                        <th scope="row">{{ count }}</th>
                                        % if event.text:
                                        <td>{{ event.text }}</td>
                                        % elif event.comment:
                                        <td>{{ event.comment }}</td>
                                        % end
                                        <td>{{ event_type }}</td>
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
            <div class="col-12">
                {{! post.body }}
            </div>
            % if post.owner:
            <div class="row">
                <div class="col-2 custom-font-size-small">
                    Asked by:
                    <p>
                        <a href="/user/{{ post.owner.id }}/{{ post.owner.clean_name }}" title="{{ post.owner.name }} detail page">{{ post.owner.name }}</a>
                        <span class="badge rounded-pill bg-primary">{{ post.owner.reputation }}</span>
                    </p>
                </div>
            </div>
            % end
        </div>
        <!-- Icon Divider-->
        <div class="divider-custom divider-light">
            <div class="divider-custom-line"></div>
            <div class="divider-custom-icon"><i class="fas fa-star"></i></div>
            <div class="divider-custom-line"></div>
        </div>

        <hr class="mt-2 mb-5">
        <div class="row justify-content-md-center">
            <div class="col-12">
                <h2>Answers</h2>
            </div>
        </div>
        % if post.answers:
        % for answer in post.answers:
        <div class="row justify-content-md-center mb-4" id="answer-id-{{ answer.post_id }}">
            <div class="col-12  border border-1">                
                {{! answer.body }}
                % if answer.owner:
                <div class="row">
                    <div class="col-2 custom-font-size-small">
                        Answered by:
                        <p>
                            <a href="/user/{{ answer.owner.id }}/{{ answer.owner.clean_name }}" title="{{ answer.owner.name }} detail page">{{ answer.owner.name }}</a>
                            <span class="badge rounded-pill bg-primary">{{ answer.owner.reputation }}</span>
                        </p>
                    </div>
                    <div class="col-2 custom-font-size-small">
                        Answer score:
                        <p>
                            % if answer.score >= 0:
                            % answer_css = 'bg-success'
                            % else:
                            % answer_css = 'bg-danger'
                            % end
                            <span class="badge rounded-pill {{ answer_css }}">{{ answer.score }}</span>
                        </p>
                    </div>
                    % if answer.post_id == post.accepted_answer_id:
                    <div class="col-2 custom-font-size-small">
                        <span class="badge rounded-pill bg-success">ACCEPTED ANSWER</span>
                    </div>
                    % end
                </div>
                % end
            </div>
        </div>
        % end
        % end
    </main>
% include('footer.tpl')