#!/usr/bin/env python3
import click
import sys
import subprocess

from instance import RetrieveInstanceIPs


@click.command()
@click.argument('jump_host')
@click.argument('jump_port')
@click.argument('identity')
@click.argument('addresses')
@click.argument('trusted', default=False)
def cli(jump_host, jump_port, identity, addresses, trusted):
    instances = []
    click.echo(' * resolving ip\'s ...')
    man = RetrieveInstanceIPs()
    for address in addresses.split(','):
        instances += man.get_ips(address)
    connect(jump_host, jump_port, identity, instances, trusted)


def connect(jump_host, jump_port, identity, instances, trusted):
    print_instances(instances)
    add_local_interfaces(instances)
    if trusted:
        connect_ssh_tunnel_trusted_channel(jump_host, jump_port, identity, instances)
    else:
        connect_ssh_tunnel(jump_host, jump_port, identity, instances)
    remove_local_interfaces(instances)


def add_local_interfaces(instances):
    click.echo(' * adding interface, user password might be needed')
    for instance in instances:
        if sys.platform == 'darwin':
            cmd = ['sudo', 'ifconfig', 'lo0', 'alias', instance.ip]
        else:
            cmd = ['sudo', 'ip', 'add', 'a', 'dev', 'lo', instance.ip]
        subprocess.call(cmd)


def remove_local_interfaces(instances):
    click.echo(' * removing interface, user/root password might be needed')
    for instance in instances:
        if sys.platform == 'darwin':
            cmd = ['sudo', 'ifconfig', 'lo0', '-alias', instance.ip]
        else:
            cmd = ['sudo', 'ip', 'addr', 'del', 'dev', 'lo', instance.ip]
        subprocess.call(cmd)


def print_instances(instances):
    click.echo('')
    for i in instances:
        click.echo('{:<10} on {:<15} port {:>5}'.format(i.name, i.ip, i.port))
    click.echo('')


def connect_ssh_tunnel(jump_host, jump_port, identity, instances):
    click.echo(' * connecting to jump host ' + jump_host + ':' + jump_port)

    opts = []

    call_ssh(jump_host, jump_port, identity, instances, opts)


def connect_ssh_tunnel_trusted_channel(jump_host, jump_port, identity, instances):
    click.echo(' * connecting to jump host ' + jump_host + ':' + jump_port)
    click.echo('WARNING: THIS OPTION DOESN\'T RESPECT KNOWN_HOSTS')

    opts = ['-o', 'ConnectTimeout 3', '-o', 'StrictHostKeyChecking no', '-o', 'UserKnownHostsFile /dev/null']

    call_ssh(jump_host, jump_port, identity, instances, opts)


def call_ssh(jump_host, jump_port, identity, instances, opts):
    for i in instances:
        opts += ['-i', identity, '-p', jump_port, '-L', '{ip}:{port}:{ip}:{port}'.format(ip=i.ip, port=i.port)]

    subprocess.call(['ssh'] + opts + [jump_host])


if __name__ == '__main__':
    cli()
