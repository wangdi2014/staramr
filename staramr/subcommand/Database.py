"""
Classes for interacting with the (ResFinder/PointFinder) databases used to detect AMR genes.
"""
import argparse
from os import path, mkdir

from staramr.SubCommand import SubCommand
from staramr.databases.AMRDatabaseHandler import AMRDatabaseHandler
from staramr.exceptions.CommandParseException import CommandParseException

"""
Base class for interacting with a database.
"""


class Database(SubCommand):

    def __init__(self, subparser, script_dir, script_name):
        """
        Builds a SubCommand for interacting with databases.
        :param subparser: The subparser to use.  Generated from argparse.ArgumentParser.add_subparsers().
        :param script_dir: The directory containing the main application script.
        :param script_name: The name of the script being run.
        """
        super().__init__(subparser, script_dir, script_name)

    def _setup_args(self, arg_parser):
        arg_parser = self._subparser.add_parser('db', help='Download ResFinder/PointFinder databases')
        subparser = arg_parser.add_subparsers(dest='db_command',
                                              help='Subcommand for ResFinder/PointFinder databases.')

        Build(subparser, self._script_dir, self._script_name + " db")
        Update(subparser, self._script_dir, self._script_name + " db")
        Info(subparser, self._script_dir, self._script_name + " db")

        return arg_parser

    def run(self, args):
        if args.db_command is None:
            self._root_arg_parser.print_help()


"""
Class for building a new database.
"""


class Build(Database):

    def __init__(self, subparser, script_dir, script_name):
        """
        Creates a SubCommand for building a new database.
        :param subparser: The subparser to use.  Generated from argparse.ArgumentParser.add_subparsers().
        :param script_dir: The directory containing the main application script.
        :param script_name: The name of the script being run.
        """
        super().__init__(subparser, script_dir, script_name)

    def _setup_args(self, arg_parser):
        name = self._script_name
        default_dir = AMRDatabaseHandler.get_default_database_directory(self._script_dir)
        epilog=("Example:\n"
               "\t"+name+" build\n"
               "\t\tBuilds a new ResFinder/PointFinder database under "+default_dir+" if it does not exist\n\n"+
               "\t"+name+" build --dir databases\n"+
               "\t\tBuilds a new ResFinder/PointFinder database under databases/")

        arg_parser = self._subparser.add_parser('build',
                                                epilog=epilog,
                                                formatter_class=argparse.RawTextHelpFormatter,
                                                help='Downloads and builds databases in the given directory.')
        arg_parser.add_argument('--dir', action='store', dest='destination', type=str,
                                help='The directory to download the databases into [' + default_dir + '].',
                                default=default_dir, required=False)
        return arg_parser

    def run(self, args):
        super(Build, self).run(args)

        if path.exists(args.destination):
            raise CommandParseException("Error, destination [" + args.destination + "] already exists",
                                        self._root_arg_parser)
        else:
            mkdir(args.destination)

        database_handler = AMRDatabaseHandler(args.destination)
        database_handler.build()


"""
Class for updating an existing database.
"""


class Update(Database):

    def __init__(self, subparser, script_dir, script_name):
        """
        Creates a SubCommand for updating an existing database.
        :param subparser: The subparser to use.  Generated from argparse.ArgumentParser.add_subparsers().
        :param script_dir: The directory containing the main application script.
        :param script_name: The name of the script being run.
        """
        super().__init__(subparser, script_dir, script_name)

    def _setup_args(self, arg_parser):
        default_dir = AMRDatabaseHandler.get_default_database_directory(self._script_dir)
        name = self._script_name
        epilog=("Example:\n"
               "\t"+name+" update databases/\n"
               "\t\tUpdates the ResFinder/PointFinder database under databases/\n\n"+
               "\t"+name+" update -d\n"+
               "\t\tUpdates the default ResFinder/PointFinder database under "+default_dir)
        arg_parser = self._subparser.add_parser('update',
                                                epilog=epilog,
                                                formatter_class=argparse.RawTextHelpFormatter,
                                                help='Updates databases in the given directories.')

        arg_parser.add_argument('-d', '--update-default', action='store_true', dest='update_default',
                                help='Updates default database directory (' + default_dir + ').', required=False)
        arg_parser.add_argument('directories', nargs=argparse.REMAINDER)

        return arg_parser

    def run(self, args):
        super(Update, self).run(args)

        if len(args.directories) == 0:
            if not args.update_default:
                raise CommandParseException("Must pass at least one directory to update", self._root_arg_parser)
            else:
                database_handler = AMRDatabaseHandler.create_default_handler(self._script_dir)
                database_handler.update()
        else:
            for directory in args.directories:
                database_handler = AMRDatabaseHandler(directory)
                database_handler.update()


"""
Class for getting information from an existing database.
"""


class Info(Database):

    def __init__(self, subparser, script_dir, script_name):
        """
        Creates a SubCommand for printing information about a database.
        :param subparser: The subparser to use.  Generated from argparse.ArgumentParser.add_subparsers().
        :param script_dir: The directory containing the main application script.
        :param script_name: The name of the script being run.
        """
        super().__init__(subparser, script_dir, script_name)

    def _setup_args(self, arg_parser):
        name = self._script_name
        default_dir = AMRDatabaseHandler.get_default_database_directory(self._script_dir)
        epilog=("Example:\n"
               "\t"+name+" info\n"
               "\t\tPrints information about the default database in "+default_dir+"\n\n"+
               "\t"+name+" info databases\n"+
               "\t\tPrints information on the database stored in databases/")
        arg_parser = self._subparser.add_parser('info',
                                                epilog=epilog,
                                                formatter_class=argparse.RawTextHelpFormatter,
                                                help='Prints information on databases in the given directories.')
        arg_parser.add_argument('directories', nargs=argparse.REMAINDER)

        return arg_parser

    def run(self, args):
        super(Info, self).run(args)

        if len(args.directories) == 0:
            database_handler = AMRDatabaseHandler.create_default_handler(self._script_dir)
            database_handler.info()
        elif len(args.directories) == 1:
            database_handler = AMRDatabaseHandler(args.directories[0])
            database_handler.info()
        else:
            for directory in args.directories:
                database_handler = AMRDatabaseHandler(directory)
                database_handler.info()
                print()