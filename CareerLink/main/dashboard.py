from admin_tools.dashboard import Dashboard, modules


class MyDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(
            modules.ModelList("Title", models=("myapp.models.MyModel",))
        )
        self.children.append(
            modules.LinkList(
                "Quick links",
                children=[
                    {"title": "Django admin", "url": "/admin/"},
                    {"title": "Google", "url": "http://www.google.com"},
                ],
            )
        )
