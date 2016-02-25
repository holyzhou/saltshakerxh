import subprocess
import os

from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from shaker.shaker_core import *
from shaker.nodegroups import *


@login_required(login_url="/account/login/")
def shell_runcmd(request):
    group = NodeGroups()
    all = group.list_groups_hosts()
    CMD = ['cmd.run', 'state.sls', 'cmd.script', 'cp.get_dir', 'cp.get_file', 'cp.get_url', 'cron.ls', 'disk.usage',
           'grains.item', 'grains.items', 'network.interface', 'service.status', 'service.start', 'service.restart',
           'service.get_all', 'state.running', 'state.highstate', 'status.uptime', 'status.meminfo', 'test.ping']
    TAG = {'deploy': 'deploy', 'scf': '/usr/bin/scf', 'f5node': '/usr/bin/f5node',
           'oic_md5': 'md5sum  /ytxt/jboss/server/default/deploy/operations-client.war',
           'uic_md5': 'md5sum  /ytxt/jboss/server/default/deploy/uic-client.war',
           'pic_md5': 'md5sum  /ytxt/jboss/server/default/deploy/productClient-1.0.4.war',
           'cic_md5': 'md5sum  /ytxt/jboss/server/default/deploy/cic-content.war', 'rollback': 'rollback'}
    return render(request, 'execute/minions_shell_runcmd.html', {'list_groups': all, 'cmds': CMD, 'tags': TAG})


@login_required(login_url="/account/login/")
def shell_result(request):
    sapi = SaltAPI()
    if request.POST:
        cmd = request.POST.get("cmd").strip()
        cmdops = request.POST.get("cmdops").strip()
        line = "################################################################"
        host_list = request.POST.getlist("hosts_name")
        host_str = ",".join(host_list)
        result = sapi.shell_remote_execution(host_str, cmdops, cmd)
        return render(request, 'execute/minions_shell_result.html', {'result': result, 'cmd': cmd, 'line': line})
    return render(request, 'execute/minions_shell_result.html')


@login_required(login_url="/account/login/")
def salt_runcmd(request):
    return render(request, 'execute/minions_salt_runcmd.html')


@login_required(login_url="/account/login/")
def salt_get(request):
    APP = ['cul', 'oic', 'cic', 'uic', 'pic', 'wap']
    return render(request, 'execute/minions_salt_get.html', {'applist': APP})


@login_required(login_url="/account/login/")
def salt_get_result(request):
    pkage = request.GET.get("project_name").strip()
    pkdate = request.GET.get("project_date").strip()
    if pkdate == "":
        pobj = subprocess.Popen('cd /srv/salt/deploy/files && python /srv/salt/deploy/files/getpackage.py %s' % pkage,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        pobj = subprocess.Popen(
            'cd /srv/salt/rollback/files && python /srv/salt/rollback/files/rollback.py %s %s' % (pkage, pkdate),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = pobj.communicate()
    return HttpResponse(result)


@login_required(login_url="/account/login/")
def salt_tools(request):
    return render(request, 'execute/minions_salt_tools.html')


@login_required(login_url="/account/login/")
def salt_pre(request):
    APP = ['cic-content', 'ReadWapPortal', 'culverin-web', 'operations-client', 'productClient-1.0.4', 'uic-client',
           'ClientWap']
    return render(request, 'execute/minions_salt_pre.html', {'applist': APP})


@login_required(login_url="/account/login/")
def salt_pre_result(request):
    sapi = SaltAPI()
    pname = request.GET.get("pj_name").strip()
    pmd5 = request.GET.get("md5_value").strip()
    if pmd5 == "":
        pmd5 = '1232443'
    get_hostip = {'cic-content': 'yf-cic-182.189read.com', 'ReadWapPortal': 'yf-wap-127.189read.com',
                  'culverin-web': 'yf-jf-129.189read.com', 'operations-client': 'yf-oic-248.189read.com',
                  'productClient-1.0.4': 'yf-pic-181.189read.com', 'uic-client': 'yf-yhzx-130.189read.com',
                  'ClientWap': 'yf-yhzx-130.189read.com'}
    host_ip = get_hostip[pname]
    result = sapi.pre_remote_execution(host_ip, pname, pmd5)
    return HttpResponse(result[host_ip])
