% err = error_message if defined('error_message') else ''

% include('header.tpl')
    <main class="container">
        <div class="row justify-content-md-center">
            <div class="col-12  mb-4">
                <div class="bg-light p-5 rounded">
                    <h1>Simple BottlePy application</h1>
                    <p class="lead">A very simple BottlePy application with SqlAlchemy support</p>
                    <a class="btn btn-lg btn-primary" href="/docs" role="button">View application docs &raquo;</a>
                </div>
                % if err:
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Error: </strong> {{ err }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                % end
            </div>
        </div>
        % if not err:
        <div class="row justify-content-md-center">
            <div class="col-12  mb-4 text-center">
                <h2>
                    Search questions
                </h2>
            </div>
        </div>
        <div class="row justify-content-md-center">
            <div class="col-12  mb-4">
                <form action="/posts" method="POST" role="form" id="searchQuestionForm" name="searchQuestionForm">
                    <div class="mb-3">
                    <label for="formNetworkSelect" class="form-label">Network</label>
                    <select class="form-select" name="network_site"  id="formNetworkSelect" aria-label="Sites select">
                        <option value="" id="networkLoading" selected="selected"></option>
                        % for network in network_sites:
                        <option value="{{ network.name }}">{{ network.value }}</option>
                        % end
                    </select>
                    <label for="formTagsSelect" class="form-label">Tags</label>
                    <select class="form-select" name="question_tag"  id="formTagsSelect" aria-label="Sites select">
                        <option value="" id="tagLoading" selected="selected">Please select network first</option>
                    </select>
                    </div>
                    <div class="mb-3">
                    <label for="formQuestionInput" class="form-label">Question</label>
                    <input type="text" class="form-control" id="formQuestionInput" name="question_title"  placeholder="Search...">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
        </div>
        % end
    </main>
% include('footer.tpl')