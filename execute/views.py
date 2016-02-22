from django.shortcuts import render,HttpResponse 
from django.contrib.auth.decorators import login_required
from shaker.shaker_core import *
from shaker.nodegroups import *
import subprocess
import os

@login_required(login_url="/account/login/")
def shell_runcmd(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    CMD = ['cmd.run', 'cmd.script', 'cp.get_dir', 'cp.get_file', 'cp.get_url', 'cron.ls','disk.usage','grains.item', 'grains.items','network.interface','service.status', 'service.start', 'service.restart', 'service.get_all','state.running', 'state.sls', 'state.highstate','status.uptime', 'status.meminfo','test.ping' ,'jobs.lookup_jid']
    return render(request, 'execute/minions_shell_runcmd.html', {'list_groups': all,'cmds':CMD})

@login_required(login_url="/account/login/")
def shell_result(request):
    sapi = SaltAPI()
    if request.POST:
        cmd = request.POST.get("cmd").strip()
	cmdops = request.POST.get("cmdops").strip()
        line = "################################################################"
        host_list = request.POST.getlist("hosts_name")
        host_str = ",".join(host_list)
        result = sapi.shell_remote_execution(host_str,cmdops,cmd)
        return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
    return render(request, 'execute/minions_shell_result.html')

@login_required(login_url="/account/login/")
def salt_runcmd(request):
    return render(request, 'execute/minions_salt_runcmd.html')
	
@login_required(login_url="/account/login/")
def salt_get(request):
    APP=['cul','oic','cic','uic','pic','wap']
    return render(request, 'execute/minions_salt_get.html',{'applist':APP})


@login_required(login_url="/account/login/")
def salt_get_result(request):
    pkage=request.GET.get("project_name").strip()
    print 'aaa'
    print pkage
    pobj = subprocess.Popen('sh /tmp/shell.sh %s && date +"%F %H:%M"' % pkage, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = pobj.communicate()
    return HttpResponse(result)


@login_required(login_url="/account/login/")
def salt_tools(request):
    return render(request, 'execute/minions_salt_tools.html')
