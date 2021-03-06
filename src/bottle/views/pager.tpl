% q_parameters = parameters if defined('parameters') else ''
% MAX_PAGE = int(records/default_result_limit)+1
% PAGES = 9
% if page_nr >= MAX_PAGE-PAGES:
%   FIRST_MENU_PAGE = MAX_PAGE-8
% else:
%   FIRST_MENU_PAGE = page_nr
% end
% if page_nr >= MAX_PAGE-PAGES:
%   LAST_MENU_PAGE = MAX_PAGE+1
% else:
%   LAST_MENU_PAGE = page_nr+PAGES
% end
% if MAX_PAGE-8 < 0:
%  FIRST_MENU_PAGE = 1
% end
% if MAX_PAGE == 1:
%  LAST_MENU_PAGE = 1
% end
% if q_parameters:
% first_page = '/{}/{}?{}'.format(page_name, str(page_nr-1), q_parameters)
% last_page = '/{}/{}?{}'.format(page_name, str(LAST_MENU_PAGE), q_parameters)
% else:
% first_page = '/{}/{}'.format(page_name, str(page_nr-1))
% last_page = '/{}/{}'.format(page_name, str(LAST_MENU_PAGE))
% end

<nav class="nav justify-content-center" aria-label="Page navigation">
    <ul class="pagination">
        % if page_nr > 1:
        <li class="page-item">
        <a class="page-link" href="{{ first_page }}" title="Go to {{ first_page }} page" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
        </a>
        </li>
        % end
        % for nav_page in range(FIRST_MENU_PAGE,LAST_MENU_PAGE):
        <%
            page_css = ''
            if q_parameters:
            page_link = '/{}/{}?{}'.format(page_name, str(nav_page), q_parameters)
            else:
            page_link = '/{}/{}'.format(page_name, str(nav_page))
            end
            if page_nr == nav_page:
                page_css = 'active'
            end
        %>
        
        <li class="page-item {{ page_css }}"><a class="page-link" href="{{ page_link }}" title="Go to {{ nav_page }} page">{{ nav_page }}</a></li>                           
        % end
        <li class="page-item">
        % if page_nr < MAX_PAGE-PAGES:
        <a class="page-link" href="{{ last_page }}"  title="Go to {{ last_page }} page" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
        </a>
        % end
        </li>
    </ul>
</nav>