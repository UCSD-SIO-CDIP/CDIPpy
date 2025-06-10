def define_env(env):
    @env.macro
    def under_construction(message="This section is under construction."):
        return f"""
<div style="border-radius:6px; overflow:hidden; margin:1em 0; font-family:inherit; box-shadow:0 1px 3px rgba(0,0,0,0.1);">
  <div style="background-color:#FFA500; color:black; padding:10px 12px; font-weight:bold; font-size:1.1em;">
    🚧 <strong>UNDER CONSTRUCTION</strong> 🚧
  </div>
  <div style="background-color:rgba(255, 165, 0, 0.15); color:black; padding:10px 12px;">
    {message}
  </div>
</div>
"""
