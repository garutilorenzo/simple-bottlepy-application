% include('header.tpl')
    <main class="container">
        <div class="row">
            <div class="col-12">
                % include('pager.tpl')
                <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Questions</th>
                      </tr>
                    </thead>
                    <tbody>
                    % for tag in tags:
                      <tr>
                        <th scope="row">{{ tag.tag_id }}</th>
                        <td><a href="/tag/{{ tag.id }}/{{ tag.clean_name }}" title="{{ tag.name }} detail page">{{ tag.name }}</a></td>
                        <td>{{ tag.questions }}</td>
                      </tr>
                    %end
                    </tbody>
                  </table>
            </div>
        </div>
    </main>
% include('footer.tpl')