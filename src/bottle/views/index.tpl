% err = error_message if defined('error_message') else ''

% include('header.tpl')
    <main class="container">
        <div class="bg-light p-5 rounded">
            <h1>Navbar example</h1>
            <p class="lead">This example is a quick exercise to illustrate how fixed to top navbar works. As you scroll, it will remain fixed to the top of your browser’s viewport.</p>
            <a class="btn btn-lg btn-primary" href="#" role="button">View navbar docs &raquo;</a>
        </div>
        % if err:
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error: </strong> {{ err }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        % end
    </main>
% include('footer.tpl')