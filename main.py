
from function import Func
from optimizer import OptimizerGA
from GUI import get_settings, info_GUI, error_GUI
from settingsGA import gaParams

global random_seed
random_seed = 1


def main():
	try:
		gaParams = get_settings()
		function = Func(gaParams.f)
		optimizer = OptimizerGA(function)
		optimizer.startGA_with_statistics(	chromosoms_number=gaParams.chromosoms_number, 
											generations_number=gaParams.generations_number, 
											mutation=gaParams.mutation, optimizer=gaParams.optimizer)
		info_GUI()

	except Exception as err:
		print('Ошибка!\n', type(err))
		print(err)
		error_GUI()


if __name__ == '__main__':
	main()


	


	
