% include('header.tpl')
    <main class="container">
        <div class="row">
          <div class="col-12 text-center">
            <h1> Users </h1>
          </div>
            <div class="col-12">
                % include('pager.tpl')
                <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Reputation</th>
                        <th scope="col">Views</th>
                        <th scope="col">UP Votes</th>
                        <th scope="col">Down Votes</th>
                        <th scope="col">Site name</th>
                      </tr>
                    </thead>
                    <tbody>
                    % for user in users:
                      <tr>
                        <th scope="row">{{ user.user_id }}</th>
                        <td><a href="/user/{{ user.id }}/{{ user.clean_name }}" title="{{ user.name }} detail page">{{ user.name }}</a></td>
                        <td>{{ user.reputation }}</td>
                        <td>{{ user.views }}</td>
                        <td>{{ user.up_votes }}</td>
                        <td>{{ user.down_votes }}</td>
                        <td>{{ user.site.name }}</td>
                      </tr>
                    %end
                    </tbody>
                  </table>
            </div>
        </div>
    </main>
% include('footer.tpl')